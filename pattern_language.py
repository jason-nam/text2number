#정규표현식 연습
from email.mime import application
import re
import into_digit 


#NR처리할 부분의 group이름은 항상 change로!!
regex_num_dictionary = [
    '([가-힣]+)점\s*[가-힣]+\s*[프로|점|퍼센트]',
    '[가-힣0-9]+점\s*([가-힣]+)\s*[프로|점|퍼센트]',
    '제([가-힣]+)\s*[항|조|목|차관|조항|항목|관|회|차]',
]
regex_text_correction = [
    ('[0-9\s]([점]\s+)[0-9]',"."),
    # ('[0-9]([\.\s]+)[0-9]',"."),
]

def apply_regular_expression(sentence: str) -> str:
    sentence_save = ""
    for regex_num in regex_num_dictionary:
        regexp = re.compile(regex_num)
        temp = regexp.search(sentence)
        re_iter = re.finditer(regex_num, sentence)
        for s in re_iter:
            sentence = sentence[:s.start()] + sentence[s.start():s.end()].replace(s.group(1), into_digit.ToDigit(s.group(1))) + sentence[s.end():]

    for regex_text in regex_text_correction:
        regexp= re.compile(regex_text[0])
        if regexp.search(sentence):
            correction_in_sentnece = regexp.findall(sentence)
            for inst in correction_in_sentnece:
                sentence = sentence.replace(inst,regex_text[1])
    return sentence

# def ApplyRegularExpression(sentence: str) -> str:
#     for regex_num in regex_num_dictionary:
#         regex = re.compile(regex_num)
#         regex_info = regex.search(sentence)
#         print(regex.findall(sentence))
#     return sentence
        

if __name__ == "__main__":
    # print(apply_regular_expression('제육 조 제이십사 항을 참고바랍니다.'))

    # print(ApplyRegularExpression('요번 시험에서 팔십삼점 오점를 받았어'))
    # print(ApplyRegularExpression('제육 조 제이십사 항을 참고바랍니다.'))
    print(apply_regular_expression("나는 이번 유 월 4일에 본 시험에서 영점 사점을 받았어."))
    print(apply_regular_expression("나는 이번 유월 사일에 본 시험에서 영점 사프로를 받았어."))
    None
