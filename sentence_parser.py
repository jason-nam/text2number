"""
STT 
"""

import sys

from phone_number import phone_number_exception 
sys.path.append("./")

import new_language
import into_digit
import pattern_language
import tag_correction
import month_exception
import text_to_list
import pos
import transform_index
import convert
import bad_words
import phone_number


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


def main(sentence: str) -> str:
    """worker function"""

    sentence = phone_number.phone_number_exception(sentence)
    sentence = new_language.apply_dictionary(sentence)
    # print('1:',sentence)
    sentence = PutNumber(sentence)
    # print('2:',sentence)
    sentence = month_exception.get_month_exception(sentence)
    # print('3:',sentence)
    sentence = pattern_language.apply_regular_expression(sentence)
    # print('4:',sentence)
    return sentence

# print(main("나는 이번 유월 사일에 본 시험에서 영점 사프로를 받았어."))
# print(main("나는 이번 시월 사일에 본 시험에서 영점 사점을 받았어."))
# print(main("이번 삼 회 추경예산안은 고용 사회안전망 강화와 경기 보강을 위해서."))
# print(main("성원이 되었으므로 제삼백칠십구 회 국회임시회 제일 차 문화체육관광위원회를 개의하겠습니다."))
# print(main("나는 지금 오십만육천원을 가지고 있어"))
# print(main("나는 이에서 시금치 이개가 나왔어"))
# print(main("삼 사 오 칠 구 십삼. 삼천칠백만원을 소비하셨습니다."))
# print(main("요번 팔월에 나는 코로나일구에 걸렸었어"))
# print(main("이 개년 동안 백범 김구 선생님께서는 백제유물을 탐방하셨다."))
# print(main("나는 이월에 이월할거야"))
# print(main("의사일정 제이 항과 문화체육관광부 및 문화재청 소관 이천이십 년도 제삼 회 추가경정예산안 의사일정 제삼 항 이천이십 년도 문화예술진흥기금운용 계획 변경안 의사일정 제사 항 이천이십 년도 영화발전기금운용 계획 변경안 의사일정 제오 항 이천이십 년도 관광진흥개발기금운용 계획 변경안"))
# print(main("내 무게는 이십삼오십스물"))
# print(main('내 전화번호는 공일공 이이이이 일일일일입니다. 니 전화번호는 뭐니?'))
# print(main('나는 삼삼오오이야'))