from function import *
from util import *


def exceptionNR(nr_list: list):
    copy = nr_list
    list_nr_but_no = [
        '하나','둘','셋','넷','다섯','여섯','일곱','여덟','아홉','열',
        '수십','수백','수천','수만','수억'
    ]
    for ind, each_nr in enumerate(nr_list):
        if each_nr != ():
            for exception in list_nr_but_no:
                if each_nr[0] == exception:
                    null_info = (each_nr[0],'')
                    copy[ind] = null_info
    return copy


def BringNumber(sentence: str) -> list:
    """문장에서 NR숫자들을 element로 가지는 list를 반환"""

    sentence_pos = apply_tag_correction(sentence)
    sentence_pos = exceptionNR(sentence_pos)
    numbers = []
    number = ""
    for ind, key in enumerate(sentence_pos):
        if key[1] == "NR":
            txt_ind = get_txt_ind(sentence, ind)
            if  sentence[txt_ind-1] == " " and number != "":
                numbers.append(number)
                number = ""
            number += key[0]
            if ind+1 == len(sentence_pos) or sentence_pos[ind+1][1] != "NR":
                numbers.append(number)
                number = ""
    return numbers


def PutNumber(sentence: str) -> str:
    """문장input에 digit대입한 문장output return"""

    numbers = remove_bad_words(BringNumber(sentence))

    if not any(number in sentence for number in numbers):
        return sentence
    for number in numbers:
        for ind, sentence_char in enumerate(sentence):
            if sentence_char != number[0]:
                continue
            pos_ind = get_pos_ind(sentence, ind)
            sentence_pos = apply_tag_correction(sentence)
            if sentence[ind:min(len(sentence),ind+len(number))] == number and sentence_pos[pos_ind][1] == "NR":
                sentence = sentence[:ind] + get_number(number) + sentence[min(len(sentence),ind+len(number)):]
                break
    return sentence