from typing import Dict

MULTIPLIERS = {
    "십": 10,
    "백": 100,
    "천": 1000,
    # "만": 10000,
    # "억": 100000000,
    # "조": 1000000000000,
    # "경": 10000000000000000,
    # "해": 100000000000000000000,
}

UNITS: Dict[str, int] = {
    "일": 1,
    "이": 2,
    "삼": 3,
    "사": 4,
    "오": 5,
    "육": 6,
    "칠": 7,
    "팔": 8,
    "구": 9,
}

UNITS_EXCEPTIONS: Dict[str, int] = {
    "륙": 6,
}

ZEROS: Dict[str, int] = {
    "영": 0,
    "공": 0,
}

NUMBERS = MULTIPLIERS.copy()
NUMBERS.update(UNITS)
NUMBERS.update(UNITS_EXCEPTIONS)
NUMBERS.update(ZEROS)

EXCEPTIONS = ["일곱"]

########################################################################

#-*- coding:utf-8 -*-

# 만 단위 자릿수
ten_thousand_pos = 4
# 억 단위 자릿수
hundred_million_pos = 9
text_digit = ['', '십', '백', '천', '만', '억']
text_decimal = '점 '

def digit2txt(arabic_num):
    korean_num = ''
    digit_count = 0
    key_list = list(UNITS.keys())
    val_list = list(UNITS.values())
    #자릿수 카운트
    for ch in arabic_num:
        # ',' 무시
        if ch == ',':
            continue
        #소숫점 까지
        elif ch == '.':
            break
        digit_count = digit_count + 1

    digit_count = digit_count-1
    index = 0

    while True:
        not_show_digit = False
        ch = arabic_num[index]
        #print(str(index) + ' ' + ch + ' ' +str(digit_count))
        # ',' 무시
        if ch == ',':
            index = index + 1
            if index >= len(arabic_num):
                break;
            continue

        if ch == '.':
            korean_num = korean_num + text_decimal
        else:
            #자릿수가 2자리이고 1이면 '일'은 표시 안함.
            # 단 '만' '억'에서는 표시 함
            if(digit_count > 1) and (digit_count != ten_thousand_pos) and  (digit_count != hundred_million_pos) and int(ch) == 1:
                korean_num = korean_num + ''
            elif int(ch) == 0:
                korean_num = korean_num + ''
                # 단 '만' '억'에서는 표시 함
                if (digit_count != ten_thousand_pos) and  (digit_count != hundred_million_pos):
                    not_show_digit = True
            else:
                korean_num = korean_num + list(UNITS.keys())[list(UNITS.values()).index(int(ch))]

        # 1억 이상
        if digit_count > hundred_million_pos:
            if not not_show_digit:
                korean_num = korean_num + text_digit[digit_count-hundred_million_pos]
        # 1만 이상
        elif digit_count > ten_thousand_pos:
            if not not_show_digit:
                korean_num = korean_num + text_digit[digit_count-ten_thousand_pos]
        else:
            if not not_show_digit:
                korean_num = korean_num + text_digit[digit_count]

        if digit_count <= 0:
            digit_count = 0
        else:
            digit_count = digit_count - 1
        index = index + 1
        if index >= len(arabic_num):
            break;
    return korean_num

########################################################################

def get_text(txt: str) -> str:
    """
    기능 설명:
    input: 문장
    output: 문장
    ex:
    >>> print(get_txt("15"))
    >>> 십오
    """
    return txt

def get_number(korean_num: str) -> str:
    current_num = 0
    num = 0
    arabic_num = ''
    if any(exception in korean_num for exception in EXCEPTIONS):
        return korean_num
    for char in korean_num:
        if char in NUMBERS:
            digit = int(NUMBERS[char])
            if char in MULTIPLIERS:
                if current_num == 0:
                    num += digit
                else:
                    num += current_num*digit
                current_num = 0
            elif char in UNITS:
                if not current_num == 0:
                    arabic_num += str(num+current_num) + " "
                    num = 0
                    current_num = digit
                else:
                    current_num += digit
            elif char in ZEROS:
                if not num == 0 or not current_num == 0:
                    arabic_num += str(num+current_num) + " " + str(digit)
                else:
                    arabic_num += str(digit) + " "
                num = 0
                current_num = 0
        else:
            if not current_num == 0 or not num == 0:
                arabic_num += str(num+current_num) + char
            else:
                arabic_num += char
            num = 0
            current_num = 0

    if not num == 0 or not current_num == 0:
        arabic_num += str(num+current_num)
    return arabic_num


if __name__ == "__main__":
    print(get_number('제구조이천오백이십삼억오백만칠천사백육십일'))
    print(get_number('이공삼공'))
    print(get_number('육조 사천억원'))
    print(get_number('제이 차관'))
    print(get_number('    이 삼 오 육'))
    print(get_number('이십삼오십스물'))
    print(get_number('공일공 팔육사육 오오오일'))

    print(digit2txt("245"))
