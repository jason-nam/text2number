from function import *
from util import *
from util.transform_index import get_txt_ind_impr
import os
_dir = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(_dir, '../../resource/bad_words.txt')

BAD_WORDS = load_list(path)

def remove_bad_words(numbers: list) -> list:
    for bad_word in BAD_WORDS:
        numbers = list(filter(lambda a: a != bad_word, numbers))
    return numbers

def exceptionNR(nr_list: list):
    copy = nr_list
    list_nr_but_no = [
        '하나','둘','셋','넷','다섯','여섯','여덟','아홉','열',
        '수십','수백','수천','수만','수억'
    ]
    for ind, each_nr in enumerate(nr_list):
        if each_nr != ():
            for exception in list_nr_but_no:
                if each_nr[0] == exception:
                    null_info = (each_nr[0],'')
                    copy[ind] = null_info
    return copy


def BringNumber(sentence: str, sentence_pos: list) -> list:
    """문장에서 NR숫자들을 element로 가지는 list를 반환"""

    sentence_pos = correct_tags(sentence, sentence_pos)
    #print(sentence_pos)
    #print(sentence_pos)
    pos_list = []
    for pos in sentence_pos:
        if pos[1] != 'NR':
            null_info=()
            pos_list.append(null_info)
        else:
            pos_list.append(pos)
    pos_list = exceptionNR(pos_list)
    string_list = []
    str = ""
    
    NR_index_in_sentence = 0
    for ind, a in enumerate(pos_list):
        b = ()
        if a != b:
            if pos_list[ind-1] != b:
                txt_ind = get_txt_ind_impr(sentence, ind)
                txt_ind2 = get_txt_ind_impr(sentence, ind-1)
                if txt_ind2 == None:
                    difference = 1
                else:   difference = txt_ind - txt_ind2 
                if difference != 1:
                    string_list.append((str,get_txt_ind_impr(sentence, NR_index_in_sentence)))
                    str=pos_list[ind][0]
                    NR_index_in_sentence = ind
                else:
                    if str == '':
                        NR_index_in_sentence = ind
                    str += a[0]
            else:
                if str =='':
                    NR_index_in_sentence = ind
                str += a[0]
        else:
            if str != '':
                string_list.append((str,get_txt_ind_impr(sentence, NR_index_in_sentence)))
                str = ''
        if pos_list[ind] != b and ind ==len(pos_list)-1:
            string_list.append((str,get_txt_ind_impr(sentence, NR_index_in_sentence)))   
    # final_list = []
    # if len(string_list)>1:
    #     final_number =string_list[0][0]
    #     first_ind = string_list[0][1]
    #     for ind in range(1,len(string_list)):
    #         between_numbers = sentence[string_list[ind-1][1]+len(string_list[ind-1][0]):string_list[ind][1]]
    #         if between_numbers.replace(" ","")=="":
    #             final_number += between_numbers+ string_list[ind][0]
    #         else:
    #             final_list.append((final_number,first_ind))
    #             final_number = string_list[ind][0]
    #             first_ind = string_list[ind][1]
    #         if ind == len(string_list)-1:
    #             final_list.append((final_number,first_ind))
    # elif len(string_list)<=1:
    #     return string_list
    # return final_list
    return string_list

def PutNumber(sentence: str, sentence_pos: list) -> str:
    """문장input에 digit대입한 문장output return"""

    numList = remove_bad_words(BringNumber(sentence, sentence_pos))
    #print(numbers)
    result =''
    ind_in_sentence = 0
    for num in numList:
        result += sentence[ind_in_sentence:num[1]] + txt_to_digit(num[0])
        ind_in_sentence = num[1] + len(num[0])
    return result + sentence[ind_in_sentence:]


# from unittest import result
# from xml.etree.ElementTree import TreeBuilder

# from transformers import QDQBERT_PRETRAINED_CONFIG_ARCHIVE_MAP
# from function import *
# from util import *


# def exceptionNR(nr_list: list):
#     copy = nr_list
#     list_nr_but_no = [
#         '하나','둘','셋','넷','다섯','여섯','일곱','여덟','아홉','열',
#         '수십','수백','수천','수만','수억'
#     ]
#     for ind, each_nr in enumerate(nr_list):
#         if each_nr != ():
#             for exception in list_nr_but_no:
#                 if each_nr[0] == exception:
#                     null_info = (each_nr[0],'')
#                     copy[ind] = null_info
#     return copy


# def BringNumber(sentence: str, sentence_pos: list) -> list:
#     """문장에서 NR숫자들을 element로 가지는 list를 반환"""

#     sentence_pos = FilterNone_toNR(sentence,FilterNR_toNone(sentence, sentence_pos))
#     sentence_pos = exceptionNR(sentence_pos)
#     numbers = []
#     number = ""
#     for ind, key in enumerate(sentence_pos):
#         if key[1] == "NR":
#             txt_ind = get_txt_ind(sentence, ind)
#             if  sentence[txt_ind-1] == " " and number != "":
#                 numbers.append(number)
#                 number = ""
#             number += key[0]
#             if ind+1 == len(sentence_pos) or sentence_pos[ind+1][1] != "NR":
#                 numbers.append(number)
#                 number = ""
#     return numbers


# def PutNumber(sentence: str, sentence_pos: list) -> str:
#     """문장input에 digit대입한 문장output return"""

#     numbers = remove_bad_words(BringNumber(sentence, sentence_pos))


#     result_sentence = ""
#     skip = 0

#     if not any(number in sentence for number in numbers):
#         return sentence

#     for ind, sentence_char in enumerate(sentence):
#         if not numbers:
#             result_sentence = result_sentence + sentence[ind+skip:]
#             break
#         if not skip == 0:

#             skip = skip - 1
#             continue
#         if sentence_char != numbers[0][0]:
#             result_sentence = result_sentence + sentence_char
#             continue

#         pos_ind = get_pos_ind(sentence, ind)

#         if sentence[ind:min(len(sentence),ind+len(numbers[0]))] == numbers[0] and sentence_pos[pos_ind][1] == "NR":
#             result_sentence = result_sentence + txt_to_digit(numbers[0])
#             skip = len(numbers[0])-1
#             numbers.pop(0)

#     return result_sentence