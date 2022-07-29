from function import *
from util import *

CALLING_CODES = ["공일공", "공일일", "공이"]


def phone_number_exception(sentence: str, sentence_pos: list) -> str:
    for calling_code in CALLING_CODES:
        if calling_code not in sentence:
            continue
        calling_code_start_indices = [i for i in range(len(sentence)) if sentence.startswith(calling_code, i)]
        for calling_code_start_index in calling_code_start_indices:
            
            sentence = sentence[:calling_code_start_index] + get_number(sentence[calling_code_start_index:calling_code_start_index+len(calling_code)+10]) + sentence[calling_code_start_index+len(calling_code)+10:]
    return sentence


if __name__ == "__main__":
    print(phone_number_exception("내 전화번호는 공일공 팔육사육 오오오일입니다. 니 전화번호는 뭐니?"))