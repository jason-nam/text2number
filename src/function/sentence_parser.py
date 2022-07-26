from function import tag_correction, convert, bad_words
from util import transform_index



def BringNumber(sentence: str) -> list:
    """문장에서 NR숫자들을 element로 가지는 list를 반환"""

    sentence_pos = tag_correction.apply_tag_correction(sentence)
    numbers = []
    number = ""
    for ind, key in enumerate(sentence_pos):
        if key[1] == "NR":
            txt_ind = transform_index.get_txt_ind(sentence, ind)
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

    numbers = bad_words.remove_bad_words(BringNumber(sentence))
    if not any(number in sentence for number in numbers):
        return sentence
    for number in numbers:
        for ind, sentence_char in enumerate(sentence):
            if sentence_char != number[0]:
                continue
            pos_ind = transform_index.get_pos_ind(sentence, ind)
            sentence_pos = tag_correction.apply_tag_correction(sentence)
            if sentence[ind:min(len(sentence),ind+len(number))] == number and sentence_pos[pos_ind][1] == "NR":
                sentence = sentence[:ind] + convert.get_number(number) + sentence[min(len(sentence),ind+len(number)):]
                break
    return sentence