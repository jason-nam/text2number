import os
import re
import random
import logging
from collections import Counter
import json

import torch
import numpy as np
from seqeval.metrics import precision_score, recall_score, f1_score, classification_report

_dir = os.path.dirname(os.path.abspath(__file__))

logger = logging.getLogger(__name__)


def get_test_texts(args):
    texts = []
    with open(os.path.join(args.data_dir, args.test_file), 'r', encoding='utf-8') as f:
        for line in f:
            text, _ = line.split('@@@')
            text = text.split()
            texts.append(text)

    return texts



def load_vocab(args):
    with open(os.path.join(_dir, "vocab/vocab.json"),"r",encoding = "UTF-8-sig") as f:
        word_vocab = json.load(f)
        # char_vocab = json.load(f)
        char_vocab = word_vocab
        
    word_ids_to_tokens, char_ids_to_tokens = [],[]
    for key in word_vocab:
        word_ids_to_tokens.append(key)
        char_ids_to_tokens.append(key)
        
    return word_vocab, char_vocab, word_ids_to_tokens, char_ids_to_tokens


# def download_w2v(args):
#     """ Download pretrained word vector """
#     w2v_path = os.path.join(args.wordvec_dir, args.w2v_file)
#     # Pretrained word vectors
#     if not os.path.exists(w2v_path):
#         logger.info("Downloading pretrained word vectors...")
#         gdown.download("https://drive.google.com/uc?id=1YX7yHm5MHZ-Icdm1ZX4X9_wD7UrXexJ-", w2v_path, quiet=False)


def get_labels(args):
    return [label.strip() for label in open(os.path.join(_dir, args.data_dir, args.label_file), 'r', encoding='utf-8')]


def load_label_vocab(args):
    label_vocab = dict()
    for idx, label in enumerate(get_labels(args)):
        label_vocab[label] = idx

    return label_vocab


def init_logger():
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(name)s -   %(message)s',
                        datefmt='%m/%d/%Y %H:%M:%S',
                        level=logging.INFO)


def set_seed(args):
    random.seed(args.seed)
    np.random.seed(args.seed)
    torch.manual_seed(args.seed)
    if not args.no_cuda and torch.cuda.is_available():
        torch.cuda.manual_seed_all(args.seed)


def compute_metrics(labels, preds):
    assert len(preds) == len(labels)
    return f1_pre_rec(labels, preds)


def f1_pre_rec(labels, preds):
    return {
        "precision": precision_score(labels, preds, suffix=True),
        "recall": recall_score(labels, preds, suffix=True),
        "f1": f1_score(labels, preds, suffix=True)
    }


def show_report(labels, preds):
    return classification_report(labels, preds, suffix=True)

def get_infer_dataset(list):
    infer_dataset = []
    for line in list:
        temp_BIO = "O "*len(line)
        temp_BIO = temp_BIO.strip()
        infer_dataset.append(line+"@@@"+temp_BIO)
    return infer_dataset
    
