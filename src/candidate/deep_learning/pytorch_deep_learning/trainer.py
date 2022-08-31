import os
import shutil
import logging
from tqdm import tqdm, trange

import numpy as np
import torch
from torch.utils.data import DataLoader, RandomSampler, SequentialSampler
from torch.optim import Adam

_dir = os.path.dirname(os.path.abspath(__file__))

# from data_loader import load_word_matrix
from .utils import set_seed, load_vocab, compute_metrics, show_report, get_labels, get_test_texts
from .model import BiLSTM_CNN_CRF

logger = logging.getLogger(__name__)


class Trainer(object):
    def __init__(self, args, train_dataset=None, dev_dataset=None, test_dataset=None, infer_dataset=None):
        self.args = args
        self.train_dataset = train_dataset
        self.dev_dataset = dev_dataset
        self.test_dataset = test_dataset
        self.infer_dataset = infer_dataset
        self.label_lst = get_labels(args)
        self.num_labels = len(self.label_lst)

        # Use cross entropy ignore index as padding label id so that only real label ids contribute to the loss later
        self.pad_token_label_id = args.ignore_index

        self.word_vocab, self.char_vocab, _, _ = load_vocab(args)
        self.pretrained_word_matrix = None
        # if not args.no_w2v:
        #     self.pretrained_word_matrix = load_word_matrix(args, self.word_vocab)

        self.model = BiLSTM_CNN_CRF(args, self.pretrained_word_matrix)

        # GPU or CPU
        self.device = "cuda" if torch.cuda.is_available() and not args.no_cuda else "cpu"
        self.model.to(self.device)

        self.test_texts = None
        if args.write_pred:
            self.test_texts = get_test_texts(args)
            # Empty the original prediction files
            if os.path.exists(args.pred_dir):
                shutil.rmtree(args.pred_dir)

    def train(self):
        train_sampler = RandomSampler(self.train_dataset)
        train_dataloader = DataLoader(self.train_dataset, sampler=train_sampler, batch_size=self.args.train_batch_size)

        # optimizer and schedule (linear warmup and decay)
        optimizer = Adam(self.model.parameters(), lr=self.args.learning_rate)

        # Train!
        logger.info("***** Running training *****")
        logger.info("  Num examples = %d", len(self.train_dataset))
        logger.info("  Num Epochs = %d", self.args.num_train_epochs)
        logger.info("  Batch size = %d", self.args.train_batch_size)

        global_step = 0
        tr_loss = 0.0
        self.model.zero_grad()

        train_iterator = trange(int(self.args.num_train_epochs), desc="Epoch")
        set_seed(self.args)

        for _ in train_iterator:
            epoch_iterator = tqdm(train_dataloader, desc="Iteration")
            for step, batch in enumerate(epoch_iterator):
                self.model.train()
                batch = tuple(t.to(self.device) for t in batch)  # GPU or CPU

                inputs = {'word_ids': batch[0],
                          'mask': batch[2],
                          'label_ids': batch[3]}
                outputs = self.model(**inputs)
                loss = outputs[0]

                loss.backward()

                tr_loss += loss.item()

                optimizer.step()
                self.model.zero_grad()
                global_step += 1

                if self.args.logging_steps > 0 and global_step % self.args.logging_steps == 0:
                    self.evaluate("test", global_step)

                if self.args.save_steps > 0 and global_step % self.args.save_steps == 0:
                    self.save_model()
        self.save_model()
        return global_step, tr_loss / global_step

    def evaluate(self, mode, step):
        if mode == 'test':
            dataset = self.test_dataset
        elif mode == 'dev':
            dataset = self.dev_dataset
        elif mode == 'train':
            dataset = self.train_dataset
        elif mode == "infer":
            dataset = self.infer_dataset
        else:
            raise Exception("Only train, dev, test and infer dataset available")

        eval_sampler = SequentialSampler(dataset)
        eval_dataloader = DataLoader(dataset, sampler=eval_sampler, batch_size=self.args.eval_batch_size)

        # Eval!
        logger.info("***** Running evaluation on %s dataset *****", mode)
        logger.info("  Num examples = %d", len(dataset))
        logger.info("  Batch size = %d", self.args.eval_batch_size)
        eval_loss = 0.0
        nb_eval_steps = 0
        preds = None
        out_label_ids = None

        for batch in tqdm(eval_dataloader, desc="Evaluating", disable=True):
            self.model.eval()
            batch = tuple(t.to(self.device) for t in batch)
            with torch.no_grad():
                inputs = {'word_ids': batch[0],
                          'mask': batch[2],
                          'label_ids': batch[3]}
                outputs = self.model(**inputs)
                tmp_eval_loss, logits = outputs[:2]

                eval_loss += tmp_eval_loss.mean().item()
            nb_eval_steps += 1
            # Slot prediction
            if preds is None:
                # decode() in `torchcrf` returns list with best index directly
                preds = np.array(self.model.crf.decode(logits, mask=inputs['mask'].byte()))
                out_label_ids = inputs["label_ids"].detach().cpu().numpy()
            else:
                try:
                    preds = np.append(preds, np.array(self.model.crf.decode(logits, mask=inputs['mask'].byte())), axis=0)
                    out_label_ids = np.append(out_label_ids, inputs["label_ids"].detach().cpu().numpy(), axis=0)
                except: 
                    print("exception")
                    eval_loss -= tmp_eval_loss.mean().item()
                    nb_eval_steps -= 1
                    continue
        eval_loss = eval_loss / nb_eval_steps
        results = {
            "loss": eval_loss
        }

        # Slot result
        slot_label_map = {i: label for i, label in enumerate(self.label_lst)}
        out_label_list = [[] for _ in range(out_label_ids.shape[0])]
        preds_list = [[] for _ in range(out_label_ids.shape[0])]
        for i in range(out_label_ids.shape[0]):
            for j in range(out_label_ids.shape[1]):
                if out_label_ids[i, j] != self.pad_token_label_id:
                    out_label_list[i].append(slot_label_map[out_label_ids[i][j]])
                    preds_list[i].append(slot_label_map[preds[i][j]])
        
        if mode == "infer":
            return preds_list
        
        if self.args.write_pred:
            if not os.path.exists(self.args.pred_dir):
                os.mkdir(self.args.pred_dir)

            # with open(os.path.join(self.args.pred_dir, "pred_{}.txt".format(step)), "w", encoding="utf-8") as f:
            #     for text, true_label, pred_label in zip(self.test_texts, out_label_list, preds_list):
            #         for t, tl, pl in zip(text, true_label, pred_label):
            #         #     f.write("{} {} {}\n".format(t, tl, pl))
            #         # f.write("\n")

        result = compute_metrics(out_label_list, preds_list)
        results.update(result)

        logger.info("***** Eval results *****")
        for key in sorted(results.keys()):
            logger.info("  %s = %s", key, str(results[key]))
        logger.info("\n" + show_report(out_label_list, preds_list))  # Get the report for each tag result

        return results

    def save_model(self):
        # Save model checkpoint (Overwrite)
        if not os.path.exists(self.args.model_dir):
            os.mkdir(self.args.model_dir)

        # Save argument
        torch.save(self.args, os.path.join(self.args.model_dir, 'args.pt'))
        # Save model for inference
        torch.save(self.model.state_dict(), os.path.join(self.args.model_dir, 'model.pt'))
        logger.info("Saving model checkpoint to {}".format(os.path.join(self.args.model_dir, 'model.pt')))

    def load_model(self):
        # Check whether model exists
        if not os.path.exists(os.path.join(_dir, self.args.model_dir)):
            raise Exception("Model doesn't exists! Train first!")

        try:
            # self.bert_config = self.config_class.from_pretrained(self.args.model_dir)
            self.args = torch.load(os.path.join(_dir, self.args.model_dir, 'args.pt'))
            logger.info("***** Args loaded *****")
            self.model.load_state_dict(torch.load(os.path.join(_dir, self.args.model_dir, 'model.pt')))
            self.model.to(self.device)
            logger.info("***** Model Loaded *****")
        except:
            raise Exception("Some model files might be missing...")

    # def infer(self, mode):
    #     if mode == "infer":
    #         dataset = self.infer_dataset
    #     else:
    #         raise Exception("Only infer dataset available")

    #     eval_sampler = SequentialSampler(dataset)
    #     eval_dataloader = DataLoader(dataset, sampler=eval_sampler, batch_size=self.args.eval_batch_size)

    #     eval_loss = 0.0
    #     nb_eval_steps = 0
    #     preds = None
    #     out_label_ids = None

    #     for batch in tqdm(eval_dataloader, desc="Evaluating"):
    #         self.model.eval()
    #         batch = tuple(t.to(self.device) for t in batch)
    #         with torch.no_grad():
    #             inputs = {'word_ids': batch[0],
    #                       'mask': batch[2],
    #                       'label_ids': batch[3]}
    #             outputs = self.model(**inputs)
    #             tmp_eval_loss, logits = outputs[:2]

    #             eval_loss += tmp_eval_loss.mean().item()
    #         nb_eval_steps += 1
    #         # Slot prediction
    #         if preds is None:
    #             # decode() in `torchcrf` returns list with best index directly
    #             preds = np.array(self.model.crf.decode(logits, mask=inputs['mask'].byte()))
    #             out_label_ids = inputs["label_ids"].detach().cpu().numpy()
    #         else:
    #             try:
    #                 preds = np.append(preds, np.array(self.model.crf.decode(logits, mask=inputs['mask'].byte())), axis=0)
    #                 out_label_ids = np.append(out_label_ids, inputs["label_ids"].detach().cpu().numpy(), axis=0)
    #             except: 
    #                 print("exception")

    #     # Slot result
    #     slot_label_map = {i: label for i, label in enumerate(self.label_lst)}
    #     out_label_list = [[] for _ in range(out_label_ids.shape[0])]
    #     preds_list = [[] for _ in range(out_label_ids.shape[0])]
    #     for i in range(out_label_ids.shape[0]):
    #         for j in range(out_label_ids.shape[1]):
    #             if out_label_ids[i, j] != self.pad_token_label_id:
    #                 out_label_list[i].append(slot_label_map[out_label_ids[i][j]])
    #                 preds_list[i].append(slot_label_map[preds[i][j]])
    #     return preds_list