
import os
from util import *
from typing  import Dict
_dir = os.path.dirname(os.path.abspath(__file__))
dict_path = os.path.join(_dir, '../../resource/new_languages.txt')

NEW_LANGUAGE: Dict[str, str] = load_dictionary(dict_path)

def apply_dictionary(sentence: str) -> str:
    if not any(dictionary_key in sentence for dictionary_key in NEW_LANGUAGE):
        return sentence
    for dictionary_key in NEW_LANGUAGE:
        sentence = sentence.replace(dictionary_key, NEW_LANGUAGE[dictionary_key]) 
    return sentence


if __name__ == "__main__":
    None