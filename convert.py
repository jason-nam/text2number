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
        "공 일 이 삼 사 오 육 칠 팔 구".split(), 0
    )
}

NUMBERS = NUMBERS = MULTIPLIERS.copy()
NUMBERS.update(UNITS)

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
                    current_num = current_num*10+digit
                else:
                    current_num += digit
        else:
            if not current_num == 0 or not num == 0:
                result += str(num+current_num) + char
            else:
                result += char
            num = 0
            current_num = 0

        # print(char, ';', num, ';', current_num, ';', result)
    if not num == 0 or not current_num == 0:
        result += str(num+current_num)
    return result


if __name__ == "__main__":
    print(get_number('제구조이천오백이십삼억오백만칠천사백육십일'))
    print(get_number('이공삼공'))
    print(get_number('육조 사천억원'))
    print(get_number('제이 차관'))
    print(get_number('    이 삼 오 육'))