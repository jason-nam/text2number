from typing import List, Dict
import pos

NUMBER: Dict[str, int] = {
    "공":0,
    "영":0,
    "일": 1,
    "이":2,
    "삼":3,
    "사":4,
    "오":5,
    "육":6,
    "칠":7,
    "팔":8,
    "구":9,
    "십":10,
    "백":100,
    "천":1000,
}

def TransformNumListToDigit(num_list: list) -> str:
    """
    digit들이 들어있는 함수를 계산한값을 str으로 반환한다.
    >>> print(TransformNumListToDigit([4,10,2])
    >>> 42
    """

    last_element = num_list[-1]
    if type(last_element) == str:
        num_list.remove(num_list[-1])
    calc = 0
    while num_list:
        max_num=max(num_list)
        max_index = num_list.index(max_num) 
        if max_index == 0:
            calc += max_num
        else:
            calc += max_num * num_list[max_index-1]
            num_list.remove(num_list[max_index -1])
        num_list.remove(max_num)
    if type(last_element)==str:
       return str(calc)+last_element
    return str(calc)


def SplitNumber(txt: str) -> list:
    """
    >>> print(SplitNumber('오십일'))
    >>> ['오','십','일']
    """

    split_number = []
    for character in txt:
        check = False
        for num in NUMBER:
            if character==num:
                split_number.append(NUMBER[num])   
                check = True
        if not check: 
            split_number.append(character)
    return split_number


def IsOneByOne(list_word_into_single_letter: list) -> list:
    """
    이공삼공과 같은 것 예외처리
    """

    is_int= False
    for i in list_word_into_single_letter:
        a = int(i)
        if a>=10:
            is_int = True
            break
    if is_int == False:
        one_by_one = ''
        for i in list_word_into_single_letter:
            one_by_one += str(i)
        return one_by_one
    return list_word_into_single_letter


def FilterException(word: str) -> list:
    """
    예외처리할 특정형태단어들 Filter
    """

    is_exception = False
    if word[0] == '제':
        is_exception = True
        return [is_exception, '제' + TransformNumListToDigit(SplitNumber(word[1:]))]
    if word[0] == '수':
        is_exception = True
        return [is_exception, '수' + TransformNumListToDigit(SplitNumber(word[1:]))]
    if word[len(word)-1] == "째":
        is_exception = True
        return [is_exception, word]
    return [is_exception, word]


def CheckAllString(list_word_split: str) -> list:
    """
    숫자라고 들어온 한글값이 모두 int로 바뀌지 못하는 str인지 확인
    """

    is_all_str = True
    for letter in list_word_split:
        if type(letter) == int:
            is_all_str = False
            break
    if is_all_str == True:
        back_to_word = ''
        for i in list_word_split:
            back_to_word +=i
        return back_to_word
    else:
        return list_word_split

def ToDigit(word: str) -> str:
    """
    외부파일에서 이 함수가 사용되어 나머지 함수들을 거친다. main함수 역할
    """

    list_word_into_single_letter = SplitNumber(word)
    if type(CheckAllString(list_word_into_single_letter)) == str:
        return CheckAllString(list_word_into_single_letter)
    #list1에 다 str일경우 과정을 안걸치고 바로 return??
    if FilterException(word)[0] == True:
        return FilterException(word)[1]
    list_for_calculation = []
    into_digit =""
    is_all_int = True
    for single_letter in list_word_into_single_letter:
        if type(single_letter) == str:
            is_all_int = False
            break
    if is_all_int == True:
        if type(IsOneByOne(list_word_into_single_letter)) == str:
            return IsOneByOne(list_word_into_single_letter)

    for single_letter in list_word_into_single_letter:
        list_for_calculation.append(single_letter)
        if type(single_letter) == str:
            into_digit += TransformNumListToDigit(list_for_calculation)
            list_for_calculation = []
    if list_for_calculation != []:
        into_digit += TransformNumListToDigit(list_for_calculation)
    return into_digit


    