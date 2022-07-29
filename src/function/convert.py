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
    "륙": 6,
    "칠": 7,
    "팔": 8,
    "구": 9,
}

ZEROS: Dict[str, int] = {
    "영": 0,
    "공": 0,
}

NUMBERS = MULTIPLIERS.copy()
NUMBERS.update(UNITS)
NUMBERS.update(ZEROS)


EXCEPTIONS = ["일곱"]

def get_txt(txt: str) -> str:
    """
    기능 설명: 
    input: 문장
    output: 문장
    ex:
    >>> print(get_txt("15"))
    >>> 십오
    """
    return txt

def get_number(word: str) -> str:
    current_num = 0
    num = 0
    result = ''
    if any(exception in word for exception in EXCEPTIONS):
        return word
    for char in word:
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
                    result +=  str(num+current_num) + " "
                    num = 0
                    current_num = digit
                else:
                    current_num += digit
            elif char in ZEROS:
                if not num == 0 or not current_num == 0:
                    result += str(num+current_num) + str(digit)
                else:
                    result += str(digit)
                num = 0
                current_num = 0
        else:
            if not current_num == 0 or not num == 0:
                result += str(num+current_num) + char
            else:
                result += char
            num = 0
            current_num = 0

    if not num == 0 or not current_num == 0:
        result += str(num+current_num)
    return result


if __name__ == "__main__":
    print(get_number('제구조이천오백이십삼억오백만칠천사백육십일'))
    print(get_number('이공삼공'))
    print(get_number('육조 사천억원'))
    print(get_number('제이 차관'))
    print(get_number('    이 삼 오 육'))
    print(get_number('이십삼오십스물'))
    print(get_number('공일공 팔육사육 오오오일'))