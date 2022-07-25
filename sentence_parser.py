"""
STT
"""

import sys 
sys.path.append("./")

import new_language
import into_digit
import pattern_language
import tag_correction
import month_exception
import text_to_list


# from hanspell import spell_checker
# from kss import split_sentences


# def space_all_list(list1):    
#     """list2 는 다 띄워쓰기, list3는 다 붙인것 (utterance모음집에서)"""
#     list2 = []
#     for utt in list1:
#         a = str(utt)
#         a = a.replace(' ','')
#         filtered = ''
#         for word in a:
#             filtered = filtered + word + ' '
#         list2.append(filtered)
#     return list2

# def no_space_list(sentences: list) -> list:
#     """remove all spaces in sentences"""

#     no_space_sentences = []
#     for sentence in sentences:
#         no_space_sentences.append(sentence.replace(" ",""))
#     return no_space_sentences

# list4는 문장분리기를 통해 forms에서 문장을 나누고 한 forms를 list형태로 묶어서 나누어주었다.
# def cut_line_list(list1):
#     list4 = []
#     ppp=0
#     for a in list1:
#         #split_sentences return []
#         output = split_sentences(a)
#         #toJSON[ppp]["Split Sentence"] = split_sentences(a)
#         list4.append(output)
#         ppp +=1
#     return list4


def exceptionNR(nr_list: list) -> list:
    """
    실제로 NR이지만 처리과정에서 그냥 digit으로 변환하지 않고 한글 그대로 출력
    """

    copy = nr_list
    list_nr_but_no = text_to_list.TextIntoList("./exception_nr.txt")
    for ind, each_nr in enumerate(nr_list):
        if each_nr != ():
            for exception in list_nr_but_no:
                if each_nr[0] == exception:
                    null_info = ()
                    copy[ind] = null_info
    return copy

def BringNumber(sentence: str) -> list:
    """
    문장에서 NR숫자들을 element로 가지는 list를 반환
    """

    #list1 = tn.checkTwo(sentence)
    list1 = tag_correction.num_two_correction(sentence)
    filtered_nr_list = []
    for a in list1:
        if a[1] == 'NR':
            filtered_nr_list.append(a)
        else:
            b=()
            filtered_nr_list.append(b)
    filtered_nr_list = exceptionNR(filtered_nr_list)
    string_list = []
    str = ''
    for a in filtered_nr_list:
        b = ()
        if a != b:
            str += a[0]
        else:
            if str != '':
                string_list.append(str)
                str = ''
    return string_list

# def PutNumber(sentence: str) -> str:
#     """
#     문장input에 digit대입한 문장output return
#     """

#     num_list = BringNumber(sentence)
#     copy = ''
#     result_sentence = ''
#     for num in num_list:
#         len_copy = len(copy)
#         while len_copy <= len(sentence)-1:
#             if sentence[len_copy] != num[0]:
#                 result_sentence += sentence[len_copy]
#                 len_copy +=1
#             else:
#                 if sentence[len_copy:len_copy+len(num)] == num:
#                     result_sentence += into_digit.ToDigit(num)
#                     copy = sentence[0:len_copy+len(num)]
#                     len_copy = len(sentence)
#                 else:
#                     result_sentence += sentence[len_copy]
#                     len_copy +=1
#     return result_sentence +sentence[len(copy):]

def PutNumber(sentence: str) -> str:
    """문장input에 digit대입한 문장output return"""

    numbers = BringNumber(sentence)
    if not all(number in sentence for number in numbers):
        return sentence
    for number in numbers:
        for ind, sentence_char in enumerate(sentence):
            if sentence_char != number[0]:
                continue
            if sentence[ind:min(len(sentence),ind+len(number))] == number:
                sentence = sentence[:ind] + into_digit.ToDigit(number) + sentence[min(len(sentence),ind+len(number)):]
    return sentence


def main(sentence: str) -> str:
    """worker function"""

    sentence=new_language.apply_dictionary(sentence)
    # print('1:',sentence)
    sentence = PutNumber(sentence)
    # print('2:',sentence)
    sentence=pattern_language.apply_regular_expression(sentence)
    # print('3:',sentence)
    sentence=month_exception.get_month_exception(sentence)
    # print('4:',sentence)
    return sentence

# print(main("나는 이번 유 일 사일에 본 시험에서 영점 사점을 받았어."))
# print(main("나는 이번 유월 사일에 본 시험에서 영점 사점을 받았어."))
# print(main("나는 이번 유 일 사일에 본 시험에서 영점 사점을 받았어."))
# print(main("이번 삼 회 추경예산안은 고용 사회안전망 강화와 경기 보강을 위해서."))
# print(main("성원이 되었으므로 제삼백칠십구 회 국회임시회 제일 차 문화체육관광위원회를 개의하겠습니다."))
# print(main("나는 지금 오십만육천원을 가지고 있어"))