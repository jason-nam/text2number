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

    input_text = "그러나 야당은 일하는 국회를 좌초시키고 코로나일구로 어려움을 겪고 있는 민생을 뒤로 하고 있습니다."
    output_text = main(input_text)
    print(output_text)