from function import sentence_parser, new_language, pattern_language, tag_correction, month_exception, phone_number

def main(sentence: str) -> str:
    """worker function"""

    sentence = phone_number.phone_number_exception(sentence)
    sentence = new_language.apply_dictionary(sentence)
    sentence = sentence_parser.PutNumber(sentence)
    sentence = month_exception.get_month_exception(sentence)
    sentence = pattern_language.apply_regular_expression(sentence)
    return sentence

if __name__ == '__main__':

    input_text = '조금이라도 관심을 갖고 사월 팔 일 날 접수하고 유월 이십육 일 이전에'
    output_text = main(input_text)
    print(output_text)