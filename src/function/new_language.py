from typing  import Dict
from util import loader

dict_path = "../data/dict/new_languages.txt"

NEW_LANGUAGE: Dict[str, str] = loader.load_dictionary(dict_path)

def apply_dictionary(sentence: str) -> str:
    if not any(dictionary_key in sentence for dictionary_key in NEW_LANGUAGE):
        return sentence
    for dictionary_key in NEW_LANGUAGE:
        sentence = sentence.replace(dictionary_key, NEW_LANGUAGE[dictionary_key]) 
    return sentence


if __name__ == "__main__":
    None