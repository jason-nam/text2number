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
    word: value
    for value, word in enumerate(
        "일 이 삼 사 오 육 칠 팔 구".split(), 1
    )
}

ZEROS: Dict[str, int] = {
    "영": 0,
    "공": 0,
}

NUMBERS = MULTIPLIERS.copy()
NUMBERS.update(UNITS)
NUMBERS.update(ZEROS)


def get_number(word):
    current_num = 0
    num = 0
    result = ''
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
                    result += str(num+current_num)
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