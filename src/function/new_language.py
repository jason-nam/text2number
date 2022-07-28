
import os

from numpy import ERR_CALL
from util import *
from typing  import Dict
_dir = os.path.dirname(os.path.abspath(__file__))
nl_dict_path = os.path.join(_dir, '../../resource/new_languages.txt')
ew_dict_path = os.path.join(_dir, '../../resource/error_words.txt')

NEW_LANGUAGE: Dict[str, str] = load_dictionary(nl_dict_path)
ERROR_WORDS: Dict[str, str] = load_dictionary(ew_dict_path)

def apply_dictionary(sentence: str) -> str:
    if not any(dictionary_key in sentence for dictionary_key in NEW_LANGUAGE):
        return sentence
    for dictionary_key in NEW_LANGUAGE:
        sentence = sentence.replace(dictionary_key, NEW_LANGUAGE[dictionary_key]) 
    return sentence

def revert_error_words(sentence: str) -> str:
    if not any(dictionary_key in sentence for dictionary_key in ERROR_WORDS):
        return sentence
    for dictionary_key in ERROR_WORDS:
        sentence = sentence.replace(dictionary_key, ERROR_WORDS[dictionary_key])
    return sentence

if __name__ == "__main__":
    None