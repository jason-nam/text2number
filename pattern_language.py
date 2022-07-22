#정규표현식 연습
import re

import os
import sys
#sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname("C:\\Users\\juna2\\text2number\\"))))
import text_to_num as tn


#NR처리할 부분의 group이름은 항상 change로!!
regex_num_dictionary = ['점(?P<change>[가-힣0-9\s]+)프로','제(?P<change>[가-힣]+)(\s)*(항|목|차관|조항|항목|관|회|차)']
regex_text_correction = [('[0-9\s](?P<dot>[점\s]+)[0-9]',"."),('[0-9](?P<dot>[\.\s]+)[0-9]',".")]

def apply_regular_expression(sentence: str) -> str:
    for regex_num in regex_num_dictionary:
        regexp = re.compile(regex_num)
        if regexp.search(sentence):
            while regexp.findall(sentence) != []:
                pattern_in_sentence = regexp.findall(sentence)
                print(pattern_in_sentence)         
                for inst in pattern_in_sentence:
                    if isinstance(inst, tuple):
                        num_text = inst[0]
                        num_text=num_text.replace(" ","")
                    else:   
                        num_text = inst.replace(" ",'')
                    #tn.get(a)가 숫자가 아니라 string으로 변환되어 나왔으면 반환하지 않게끔
                    sentence = sentence.replace(num_text, tn.get(num_text))
    for regex_text in regex_text_correction:
        regexp= re.compile(regex_text[0])
        if regexp.search(sentence):
            correction_in_sentnece = regexp.findall(sentence)
            for inst in correction_in_sentnece:
                sentence = sentence.replace(inst,regex_text[1])
    return sentence


print(apply_regular_expression("성원이 되었으므로 제삼백칠십구 회 국회임시회 제일 차 문화체육관광위원회를 개의하겠습니다."))
