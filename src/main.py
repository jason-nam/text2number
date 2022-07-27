from function import sentence_parser, new_language, pattern_language, month_exception, phone_number, tag_correction

from util import transform_index, pos
import time

def main(sentence: str) -> str:
    """worker function"""
    #문장 분리
    #돌리고
    #합치고
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

    input_text = "허리나 요충사업원 "
    # input_text = "작년에 우리 백제미소불 환수 관련해 가지고 얘기를 했는데 지금"
    start = time.time()  # 시작 시간 저장
    output_text = main(input_text)
    print("time :", time.time() - start)  # 현재시각 - 시작시간 = 실행 시간
    print(output_text)
    print(pos.get_pos(input_text))
    None
