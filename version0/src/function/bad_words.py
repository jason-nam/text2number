import os
from util import *
_dir = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(_dir, '../../resource/bad_words.txt')

BAD_WORDS = load_list(path)

def remove_bad_words(numbers: list) -> list:
    for bad_word in BAD_WORDS:
        numbers = list(filter(lambda a: a != bad_word, numbers))
    return numbers

