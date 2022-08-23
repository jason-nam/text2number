from function import *
from util import *

CALLING_CODES = ["공일공", "공일일", "공이"]
NUMBER_KOREAN = ["공","일","이","삼","사","오","육","칠","팔","구","영","하나","둘","셋","넷","다섯","여섯","일곱","여덟","아홉"]
SPEACIAL_LETTER = ["다시","-","에"]
'''
def phone_number_exception(sentence: str, sentence_pos: list) -> str:
    for calling_code in CALLING_CODES:
        if calling_code not in sentence:
            continue
        calling_code_start_indices = [i for i in range(len(sentence)) if sentence.startswith(calling_code, i)]
        for calling_code_start_index in calling_code_start_indices:
            
            sentence = sentence[:calling_code_start_index] + txt_to_digit(sentence[calling_code_start_index:calling_code_start_index+len(calling_code)+10]) + sentence[calling_code_start_index+len(calling_code)+10:]
    return sentence
'''
def PhoneNumberToDigit(sentence):
    began = False
    number_count = 0
    ind_in_sentence = 0
    str = ''
    starting_index = -1
    last_index = -1
    brough_number = ''

    while ind_in_sentence <= len(sentence) - 1:
        # print("B")
        if sentence[ind_in_sentence] in SPEACIAL_LETTER:
            ind_in_sentence += 1
            if (
                number_count == 3 
                or number_count == 7
            ):
                continue
            else:
                str = ''
                number_count = 0
                continue
        if sentence[ind_in_sentence:ind_in_sentence + 2] in SPEACIAL_LETTER:
            ind_in_sentence += 2
            if (
                number_count == 3 
                or number_count == 7
            ):
                continue
            else:
                str = ''
                number_count = 0
                continue
        if sentence[ind_in_sentence:ind_in_sentence + 2] in NUMBER_KOREAN:
            if str == '':
                starting_index = ind_in_sentence
            str += sentence[ind_in_sentence:ind_in_sentence + 2]
            ind_in_sentence += 2
            number_count += 1
            if ind_in_sentence > len(sentence) - 1:
                last_index = ind_in_sentence - 2
                brough_number = str
                break
            continue
        if sentence[ind_in_sentence:ind_in_sentence + 1] in NUMBER_KOREAN:
            if str == '':
                starting_index = ind_in_sentence
            str += sentence[ind_in_sentence:ind_in_sentence + 1]
            ind_in_sentence += 1
            number_count += 1
            if ind_in_sentence > len(sentence) - 1:
                last_index = ind_in_sentence - 1
                brough_number = str
                break
            continue
        if number_count == 11:
            last_index = ind_in_sentence - 1
            brough_number = str
            break
        if sentence[ind_in_sentence] == " ":
            ind_in_sentence += 1
            continue
        str = ''
        number_count = 0
        ind_in_sentence += 1
    phone_number_in_digit = ''
    #brough_number = sentence[starting_index:last_index+1]
    brough_number = brough_number.replace(" ","")
    if number_count == 11:
        while brough_number != '':
            if brough_number[0] in NUMBER_KOREAN:
                phone_number_in_digit += repr((NUMBER_KOREAN.index(brough_number[0])) % 10)
                brough_number = brough_number[1:]
            if brough_number[0:2] in NUMBER_KOREAN:
                phone_number_in_digit += repr((NUMBER_KOREAN.index(brough_number[0:2])) % 10)
                brough_number = brough_number[2:]
        phone_number_in_digit = (
            phone_number_in_digit[0:3] 
            + '-' 
            + phone_number_in_digit[3:7] 
            + "-"
            + phone_number_in_digit[7:]
        )
        return sentence[:starting_index] + phone_number_in_digit + sentence[last_index + 1:]
        #한글을 숫자로 바꾸는 함수
    return sentence

def ApplyPhoneNumberDigit(sentence):
    while sentence != PhoneNumberToDigit(sentence):
        sentence = PhoneNumberToDigit(sentence)
    return sentence
        


if __name__ == "__main__":
    print(ApplyPhoneNumberDigit("내 전화번호는 공 일   공 에 팔 육 사 육 오오오일입니다. 니 전화번호는 뭐니? 내거는 공일공에 이칠팔육 오삼 육팔 로"))
