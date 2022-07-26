from posixpath import split
from function import sentence_parser, new_language, pattern_language, month_exception, phone_number, tag_correction

from util import transform_index, pos

def main(sentence: str) -> str:
    """worker function"""
    #문장 분리
    #돌리고
    #합치고
    nominative_case_pos_tags = ["JKS", "JKC", "JX", "JKO" ] #JKG (?)
    nominative_case_pos_keys = ["의","이", "은", "는", "을", "를", "가"]
    sentence_pos = tag_correction.apply_tag_correction(sentence)

    # print(sentence_pos)

    split_sentence = []
    result_sentence = ""
    sentence_start_index = 0
    sentence_end_index = 0
    for pos_index, pos_element in enumerate(sentence_pos):
        if any(nominative_case_pos_key == pos_element[0] for nominative_case_pos_key in nominative_case_pos_keys) and any(nominative_case_pos_tag == pos_element[1] for nominative_case_pos_tag in nominative_case_pos_tags):
            sentence_end_index = transform_index.get_txt_ind(sentence, pos_index)+1
            split_sentence.append(sentence[sentence_start_index:sentence_end_index])
            sentence_start_index = sentence_end_index
    split_sentence.append(sentence[sentence_start_index:])

    for i in range(len(split_sentence)):
        split_sentence[i] = phone_number.phone_number_exception(split_sentence[i])
        split_sentence[i] = new_language.apply_dictionary(split_sentence[i])
        split_sentence[i] = sentence_parser.PutNumber(split_sentence[i])
        split_sentence[i] = month_exception.get_month_exception(split_sentence[i])
        split_sentence[i] = pattern_language.apply_regular_expression(split_sentence[i])
        result_sentence += split_sentence[i]
    return result_sentence

if __name__ == '__main__':

    # input_text = "우리 제일 법안심사 소위원회는 지난 사월 이십팔 일 총 팔십한 건의 법률안을 심사하여 한 건은 수정안으로 채택하고 스물일곱 건은 통합 조정하여 두 건의 대안으로 제안하기로 의결하였습니다."

    # input_text = "지난 일월 이십이 일 국가공무원법 제삼십일 조의 이에 따라 대통령이 제출하고 일월 이십오 일 국회법 제육십오 조의 이에 따라 우리 위원회에 회부된 문화체육관광부 장관 후보자에 대한 인사청문회를 실시하기 위한 것입니다."
    # output_text = main(input_text)
    # print(output_text)
    None