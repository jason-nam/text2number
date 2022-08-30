from typing import Tuple, List
import argparse

from .pytorch_deep_learning import main


def parse_result(sent, infer_tag):
    infer_sent = ""
    num_key = ""
    num_ind = None
    num = []
    # print(len(infer_tag))
    # print(len(sent))
    # print(infer_tag)
    # print(sent)
    for i, c in enumerate(sent):
        if (
            infer_tag[i] == "B" 
            and i == len(sent) - 1
        ):
            infer_sent = infer_sent + "[" + c + "]"
            num_ind = i
            num_key = num_key + c
            num.append((num_key, num_ind))
        elif (
            infer_tag[i] == "I" 
            and i == len(sent) - 1
        ):
            infer_sent = infer_sent + c + "]"
            num_key = num_key + c
            num.append((num_key, num_ind))
        elif (
            i != 0
            and infer_tag[i] == "B" 
            and infer_tag[i-1] == "I"
        ):
            infer_sent = infer_sent + "]" + "[" + c
            num.append((num_key, num_ind))
            num_key = c
            num_ind = i
        elif infer_tag[i] == "B":
            infer_sent = infer_sent + "[" + c
            num_ind = i
            num_key = num_key + c
        elif (
            not i == 0 
            and infer_tag[i] == "O" 
            and infer_tag[i-1] in ("B", "I")
        ):
            infer_sent = infer_sent + "]" + c
            num.append((num_key, num_ind))
            num_key = ""
            num_ind = None
        elif infer_tag[i] == "I":
            infer_sent = infer_sent + c
            num_key = num_key + c
        else:
            infer_sent = infer_sent + c
    return infer_sent, num


def deep_candidate(sent: str):
    
    parser = argparse.ArgumentParser()

    parser.add_argument("--data_dir", default="./data", type=str, help="The input data dir")
    parser.add_argument("--model_dir", default="./model", type=str, help="Path for saving model")
    parser.add_argument("--wordvec_dir", default="./wordvec", type=str, help="Path for pretrained word vector")
    parser.add_argument("--vocab_dir", default="./vocab", type=str)
    parser.add_argument("--pred_dir", default="./preds", type=str, help="The prediction file dir")

    parser.add_argument("--train_file", default="train.tsv", type=str, help="Train file")
    parser.add_argument("--test_file", default="test.tsv", type=str, help="Test file")    
    parser.add_argument("--infer_file", default="infer.tsv", type=str, help="Infer file")
    parser.add_argument("--label_file", default="label.txt", type=str, help="Label file")
    parser.add_argument("--w2v_file", default="word_vector_300d.vec", type=str, help="Pretrained word vector file")
    parser.add_argument("--write_pred", action="store_true", help="Write prediction during evaluation")

    parser.add_argument("--max_seq_len", default=250, type=int, help="Max sentence length")
    parser.add_argument("--max_word_len", default=10, type=int, help="Max word length")
    parser.add_argument("--word_vocab_size", default=100000, type=int, help="Maximum size of word vocabulary")
    parser.add_argument("--char_vocab_size", default=1000, type=int, help="Maximum size of character vocabulary")

    parser.add_argument("--word_emb_dim", default=300, type=int, help="Word embedding size")
    parser.add_argument("--char_emb_dim", default=30, type=int, help="Character embedding size")
    parser.add_argument("--final_char_dim", default=50, type=int, help="Dimension of character cnn output")
    parser.add_argument("--hidden_dim", default=350, type=int, help="Dimension of BiLSTM output")

    parser.add_argument("--kernel_lst", default="2,3,4", type=str, help="kernel size for character cnn")
    parser.add_argument("--num_filters", default=32, type=int, help=" Number of filters for character cnn")

    parser.add_argument('--seed', type=int, default=42, help="random seed for initialization")
    parser.add_argument("--train_batch_size", default=2048, type=int, help="Batch size for training")
    parser.add_argument("--eval_batch_size", default=128, type=int, help="Batch size for evaluation")
    parser.add_argument("--infer_batch_size", default=1, type=int, help="Batch size for inference")
    parser.add_argument("--learning_rate", default=0.005, type=float, help="The initial learning rate")
    parser.add_argument("--num_train_epochs", default=1.0, type=float, help="Total number of training epochs to perform.")
    parser.add_argument("--slot_pad_label", default="PAD", type=str, help="Pad token for slot label pad (to be ignore when calculate loss)")
    parser.add_argument("--ignore_index", default=0, type=int,
                        help='Specifies a target value that is ignored and does not contribute to the input gradient')

    parser.add_argument('--logging_steps', type=int, default=1200, help="Log every X updates steps.")
    parser.add_argument('--save_steps', type=int, default=1200, help="Save checkpoint every X updates steps.")

    parser.add_argument("--do_train", action="store_true", help="Whether to run training.")
    parser.add_argument("--do_eval", action="store_true", help="Whether to run eval on the test set.")
    parser.add_argument("--do_infer", action="store_true", default=True, help="Whether to run infer on the infer set.")
    parser.add_argument("--no_cuda", action="store_true", help="Avoid using CUDA when available")
    parser.add_argument("--no_w2v", action="store_true", help="Not loading pretrained word vector")

    args = parser.parse_args()

    infer_tag = main(args, sent)[0]

    return parse_result(sent, infer_tag)


if __name__ == "__main__":
    sent = "삼백육십오일 동안 무엇을 했는가"
    print(deep_candidate(sent))