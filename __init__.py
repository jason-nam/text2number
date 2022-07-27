import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from src.function import sentence_parser, new_language, pattern_language, month_exception, phone_number

def korean2num(sentence: str) -> str:
    """worker function"""

    sentence = phone_number.phone_number_exception(sentence)
    sentence = new_language.apply_dictionary(sentence)
    sentence = sentence_parser.PutNumber(sentence)
    sentence = month_exception.get_month_exception(sentence)
    sentence = pattern_language.apply_regular_expression(sentence)
    return sentence

if __name__ == '__main__':
    text = [
        '내 전화번호는 공일공 팔육사육 오오오일입니다. 니 전화번호는 뭐니?',
        '나는 이번 유 월 사일에 본 시험에서 구점 사점을 받았어.',
        '기상청에서는 올 이월에도 꽃샘추위가 몇 차례 찾아올 것이라고 전망하였다'
    ]
    for item in text:
        print(item)
        item = korean2num(item)
        print(item)
        print()
