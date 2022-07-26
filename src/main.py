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


    input_text = '우리는 삼삼오오 모였다.'
    output_text = main(input_text)
    print(output_text)