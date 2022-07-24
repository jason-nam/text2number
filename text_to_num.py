#from xml.etree.ElementTree import TreeBuilderng
#[300,4,10] - >340 str
from typing import List, Dict
from pos import get_pos

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


def transform_numlist_txt(num_list):
    """
    input: list
    output: str
    """
    L2 = num_list
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

def split_num(txt):
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
        
def get(ha):
    list1=[]
    list1 = split_num(ha)
    all_str = True
    for i in list1:
        if type(i) == int:
            all_str = False
            break
    if all_str == True:
        s = ''
        for i in list1:
            s +=i
        return s
    #list1에 다 str일경우 과정을 안걸치고 바로 return??
    list2 = []
    final =""
    if ha[0] == '제':
        return '제' + transform_numlist_txt(split_num(ha[1:]))
    if ha[len(ha)-1] == "째":
        return ha
    
    boo = True
    for i in list1:
        if type(i) == str:
            boo = False
            break
    if boo == True:
        boo= False
        for i in list1:
            a = int(i)
            if a>=10:
                boo = True
                break
        if boo == False:
            sleep = ''
            for i in list1:
                sleep += str(i)
            #print(sleep)
            return sleep
    for a in list1:
        list2.append(a)
        if type(a) == str:
            final += transform_numlist_txt(list2)
            list2 = []
    if list2 != []:
        final += transform_numlist_txt(list2)
    return final