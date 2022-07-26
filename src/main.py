from function import sentence_parser, new_language, pattern_language, tag_correction, month_exception, phone_number

def main(sentence: str) -> str:
    """worker function"""
    #문장 분리
    #돌리고
    #합치고

    sentence = phone_number.phone_number_exception(sentence)
    sentence = new_language.apply_dictionary(sentence)
    sentence = sentence_parser.PutNumber(sentence)
    sentence = month_exception.get_month_exception(sentence)
    sentence = pattern_language.apply_regular_expression(sentence)
    return sentence

if __name__ == '__main__':

    input_text = "우리 제일 법안심사 소위원회는 "
    output_text = main(input_text)
    print(output_text)

    input_text = "지난 사월 이십팔 일 총 팔십한 건의 법률안을 "
    output_text = main(input_text)
    print(output_text)

    input_text = "심사하여 한 건은 "
    output_text = main(input_text)
    print(output_text)
    input_text = "수정안으로 채택하고 스물일곱 건은 "
    output_text = main(input_text)
    print(output_text)

    input_text = "통합 조정하여 두 건의 대안으로 제안하기로 의결하였습니다."
    output_text = main(input_text)
    print(output_text)