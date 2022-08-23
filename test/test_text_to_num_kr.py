"""
Test the ``text_to_num`` library.
"""
from unittest import TestCase
from random import randint
from src_temp.text_to_num import text2num

def num2text(count: str):
    nstring = ["", "십", "백", "천", "만", "십", "백", "천", "억", "십", "백", "천", "조", "십", "백", "천"]
    nlist = list(count)
    nlen = len(count)
    stringnum = ""
    nd = {"1": "일", "2": "이", "3": "삼", "4": "사", "5": "오", "6": "육", "7": "칠", "8": "팔", "9": "구", "0": ""}
    carry = False
    nlen = nlen - 1
    for i in nlist:
        if i == "0":
            if (
                nstring[nlen] in ("만", "억", "조")
                and carry
            ):
                stringnum = stringnum + nd[i] + nstring[nlen]
        else:
            if (
                nd[i] == "일" 
                and nstring[nlen] not in ("", "만", "억", "조")
            ):
                stringnum = stringnum + nstring[nlen]
            else:
                stringnum = stringnum + nd[i] + nstring[nlen]
            carry = True
        if nstring[nlen] in ("만", "억", "조"):
            carry = False
        nlen -= 1
    return stringnum

# for _ in range(1000):
# while True:
#     count = randint(0, 1_0000_0000_0000_0000)
#     numkr = num2text(count=str(count))
#     print(count)
#     try:
#         num = text2num(numkr, "kr")
#     except:
#         raise

#     if num != count:
#         print(num)
#         raise

class TestTextToNumEN(TestCase):
    def test_text2num(self):
        num1 = 53_000_243_724
        test1 = num2text(str(num1))
        self.assertEqual(text2num(test1, "kr"), num1)

        num2 = 51_578_302
        test2 = num2text(str(num2))
        self.assertEqual(text2num(test2, "kr"), num2)

