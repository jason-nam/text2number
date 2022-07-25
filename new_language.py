from typing  import Dict


DICTIONARY: Dict[str, str] = {
    "코로나일구" : "코로나19",
    "이공삼공" : "2030",
    "육이오" : "6.25",
    "삼일절" : "3.1절",
    "사일구혁명" : "4.19혁명",
    "지세번" : "G7"
}


def apply_dictionary(sentence: str) -> str:
    if not any(dictionary_key in sentence for dictionary_key in DICTIONARY):
        return sentence
    for dictionary_key in DICTIONARY:
        sentence = sentence.replace(dictionary_key, DICTIONARY[dictionary_key]) 
    return sentence

if __name__ == "__main__":
    None