"""
Test the ``text_to_num`` library.
"""
from unittest import TestCase, main
from random import randint
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.text_to_num import text2num


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


class TestTextToNumKR(TestCase):
    def test_text2num(self):
        num1 = 530_0024_3724
        test1 = num2text(str(num1))
        self.assertEqual(text2num(test1, "kr"), num1)

        num2 = 5157_8302
        test2 = num2text(str(num2))
        self.assertEqual(text2num(test2, "kr"), num2)

        self.assertEqual(text2num("팔십오", "kr"), 85)
        self.assertEqual(text2num("천백십일경천백십일조천백십일억천백십일만천백십일", "kr"), 1111_1111_1111_1111_1111)

        self.assertEqual(text2num("경", "kr"), 1_0000_0000_0000_0000)
        self.assertEqual(text2num("조", "kr"), 1_0000_0000_0000)
        self.assertEqual(text2num("억", "kr"), 1_0000_0000)
        self.assertEqual(text2num("만", "kr"), 1_0000)
        self.assertEqual(text2num("경조억만", "kr"), 1_0001_0001_0001_0000)

        self.assertEqual(text2num("만일", "kr"), 1_0001)
        self.assertEqual(text2num("조일", "kr"), 1_0000_0000_0001)
        self.assertEqual(text2num("경일", "kr"), 1_0000_0000_0000_0001)
        self.assertEqual(text2num("해일", "kr"), 1_0000_0000_0000_0000_0001)
        

    def test_text2num_zeroes(self):
        self.assertEqual(text2num("영", "kr"), 0)
        self.assertEqual(text2num("공일", "kr"), 1)
        self.assertEqual(text2num("영천백십일", "kr"), 1111)
        self.assertRaises(ValueError, text2num, "십영", "kr")
        self.assertRaises(ValueError, text2num, "백영십일", "kr")
        self.assertRaises(ValueError, text2num, "천백십영", "kr")


    def test_text2num_exceptions(self):
        self.assertRaises(ValueError, text2num, "천천백십일", "kr")
        self.assertRaises(ValueError, text2num, "십오오십", "kr")
        self.assertRaises(ValueError, text2num, "십오십", "kr")
        self.assertRaises(ValueError, text2num, "십십", "kr")
        self.assertRaises(ValueError, text2num, "백천", "kr")
        self.assertRaises(ValueError, text2num, "오십백", "kr")


if __name__ == "__main__":
    main()

    