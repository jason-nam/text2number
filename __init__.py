import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from src.function import sentence_parser, new_language, pattern_language, month_exception, phone_number, tag_correction
from src.util import transform_index

def korean2num(sentence: str) -> str:
    """worker function"""

    nominative_case_pos_tags = ["JKS", "JKC", "JX", "JKO" ] #JKG (?)
    nominative_case_pos_keys = ["이", "은", "는", "을", "를", "가"]
    sentence_pos = tag_correction.apply_tag_correction(sentence)

    # print(sentence_pos)

    split_sentence = []
    result_sentence = ""
    sentence_start_index = 0
    sentence_end_index = 0
    for pos_index, pos_element in enumerate(sentence_pos):
        if any(nominative_case_pos_key == pos_element[0] for nominative_case_pos_key in nominative_case_pos_keys) and any(nominative_case_pos_tag == pos_element[1] for nominative_case_pos_tag in nominative_case_pos_tags):
            sentence_end_index = transform_index.get_txt_ind_impr(sentence, pos_index) + 2
            split_sentence.append(sentence[sentence_start_index:sentence_end_index])
            sentence_start_index = sentence_end_index
    split_sentence.append(sentence[sentence_start_index:])

    for i in range(len(split_sentence)):
        split_sentence[i] = phone_number.phone_number_exception(split_sentence[i])
        split_sentence[i] = new_language.apply_dictionary(split_sentence[i])
        split_sentence[i] = pattern_language.apply_regular_expression_before_convert(split_sentence[i])
        split_sentence[i] = sentence_parser.PutNumber(split_sentence[i])
        split_sentence[i] = month_exception.get_month_exception(split_sentence[i])
        split_sentence[i] = pattern_language.apply_regular_expression(split_sentence[i])
        result_sentence += split_sentence[i]
    return result_sentence

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
