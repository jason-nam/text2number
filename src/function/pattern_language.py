import re
from typing import Dict, List
from function import *

TIME_REGEX = [
    # day, month, year
    "([일|이|삼|사|오|육|칠|팔|구|십|백|천|만|억]{1,})\s*년",
    "[영|일|이|삼|사|오|육|유|칠|팔|구|시|십]{1,2}\s{0,1}월\s{0,1}([일|이|삼|사|오|육|칠|팔|구|십]{1,})\s{0,1}일", # "...구 월 이십일..."
    "[가-힣|0-9]+\s{0,1}년\s{0,1}([가-힣|0-9]+[일]*)\s{0,1}(?:일+)", # "...이천이십이년 이십일일..."
    "([영|일|이|삼|사|오|육|유|칠|팔|구|시|십]{1,2})\s{0,1}월[^하했할]" # "...사 월에는..."
]

UNIT_REGEX = [
    # percent, gram, kilo, etc
    '([가-힣|0-9]+)\s*점\s*[가-힣|0-9]+\s*(프로|점|퍼센트|그람|킬로)', # "...구점 일 프로..."
    '[가-힣|0-9]+\s*점\s*([가-힣|0-9]+)\s*(프로|점|퍼센트|그람|킬로)', # "...9 점 일 프로..."
    '([영|일|이|삼|사|오|육|칠|팔|구|십|백|천|만|억|조]{1,})\s*분의\s*[영|일|이|삼|사|오|육|칠|팔|구|십|백|천|만|억|조]{1,}',
    '[0-9]\s*분의\s*([영|일|이|삼|사|오|육|칠|팔|구|십|백|천|만|억|조]{1,})',
]

COUNT_REGEX = [
    # 제 _ 항/조 etc
    '\s제([영|일|이|삼|사|오|육|칠|팔|구|십|백|천|만|억|조|해|경]{1,})\s{0,1}[항|조|목|차관|조항|항목|관|회|차|법안심사]', # "...제 삼백칠십 항..."
    '^제([영|일|이|삼|사|오|육|칠|팔|구|십|백|천|만|억|조|해|경]{1,})\s{0,1}[항|조|목|차관|조항|항목|관|회|차|법안심사]', # "제 삼백칠십 항..."
    '전과\s{0,1}([영|일|이|삼|사|오|육|칠|팔|구|십|백|천]{1,})\s{0,1}범', # "...전과 구..."
    '([영|일|이|삼|사|오|육|륙|칠|팔|구|십|백|천]{1,})\s*다시\s*[영|일|이|삼|사|오|육|륙|칠|팔|구|십|백|천]{1,}',
    '[0-9]\s*다시\s*([영|일|이|삼|사|오|육|륙|칠|팔|구|십|백|천]{1,})',
]

ID_NUMBER_REGEX = [
    '([공|영|일|이|삼|사|오|육|칠|팔|구]{2,3}\s{0,1}[공|영|일|이|삼|사|오|육|칠|팔|구]{3,4}\s{0,1}[공|영|일|이|삼|사|오|육|칠|팔|구]{4})', # "...공일공 이이이이 일일일일..."
    '([공|영|일|이|삼|사|오|육|칠|팔|구]{3}\s*다시\s*[공|영|일|이|삼|사|오|육|칠|팔|구]{2,4}\s*다시\s*[공|영|일|이|삼|사|오|육|칠|팔|구]{4,5})', # 사업자 번호
]

CONVERT_REGEX = TIME_REGEX.copy()
CONVERT_REGEX.extend(UNIT_REGEX)
CONVERT_REGEX.extend(COUNT_REGEX)
CONVERT_REGEX.extend(ID_NUMBER_REGEX)

# print(CONVERT_REGEX)

REVERT_REGEX = [
    # 아라비아 숫자를 다시 한글로 변환
    '([14]|10{1})\s{0,1}시', # "...내 눈은 4시가 아니다..."
    '(2)번',
    '(1)\s{0,1}때',
]

CONVERT_TEXT_REGEX: Dict[str, str] = {
    # 문자가 기호 등 으로 변환
    '[0-9\s](\s*점\s+)[0-9]': ".", # "...6 점 5..."
    '[0-9](\s*다시\s*)[0-9]': "-", # "...6 다시 5..."
    # '[0-9](\s*분의\s*)[0-9]' : "/",
}

def convert_regular_expression(sentence: str) -> str:
    for regex_num in CONVERT_REGEX:
        re_iter = re.finditer(regex_num, sentence)
        for s in re_iter:
            # print(sentence)
            # print(s.group(1))
            start = s.span(1)[0]
            end = s.span(1)[1]
            sentence = sentence[:start] + sentence[start:end].replace(s.group(1), txt_to_digit(s.group(1))) + sentence[end:]
    return sentence

def revert_regular_expression(sentence: str) -> str:
    for regex_num in REVERT_REGEX:
        re_iter = re.finditer(regex_num, sentence)
        for s in re_iter:
            # print(sentence)
            # print(s.group(1))
            start = s.span(1)[0]
            end = s.span(1)[1]
            sentence = sentence[:start] + sentence[start:end].replace(s.group(1), digit_to_txt(s.group(1))) + sentence[end:]
    return sentence

def convert_text_regular_expression(sentence: str) -> str:
    for regex_text in CONVERT_TEXT_REGEX:
        re_iter_text = re.finditer(regex_text, sentence)
        for s in re_iter_text:
            # print(sentence)
            # print(s.group(1))
            start = s.span(1)[0]
            end = s.span(1)[1]
            sentence = sentence[:start] + sentence[start:end].replace(s.group(1), CONVERT_TEXT_REGEX[regex_text]) + sentence[end:]
    return sentence

if __name__ == "__main__":
    None


# REGEX_NUMBERS_AFTER_CONVERT = [
#     '([가-힣|0-9]+)\s*점\s*[가-힣|0-9]+\s*(프로|점|퍼센트|그람|킬로)',
#     '[가-힣|0-9]+\s*점\s*([가-힣|0-9]+)\s*(프로|점|퍼센트|그람|킬로)',
#     '\s제([영|일|이|삼|사|오|육|칠|팔|구|십|백|천|만|억|조|해|경]{1,})\s*[항|조|목|차관|조항|항목|관|회|차|법안심사]',
#     '^제([영|일|이|삼|사|오|육|칠|팔|구|십|백|천|만|억|조|해|경]{1,})\s*[항|조|목|차관|조항|항목|관|회|차|법안심사]',

#     # '\s제([가-힣]+)\s*[항|조|목|차관|조항|항목|관|회|차|법안심사]',
#     '전과\s{0,1}([영|일|이|삼|사|오|육|칠|팔|구|십|백|천]{1,})\s{0,1}범',
# ]

# PASS_NUMBERS = [
#     '([0|1|2|3|4|5|6|7|8|9|10]{1})\s*시', #[몇]시
# ]

# REGEX_NUMBERS_BEFORE_CONVERT = [
#     '[가-힣|0-9]+\s{0,1}월\s{0,1}([가-힣|0-9]+[일]*)\s{0,1}(일+)',
#     '[가-힣|0-9]+\s{0,1}년\s{0,1}([가-힣|0-9]+[일]*)\s{0,1}(일+)'
# ]

# REGEX_TEXT_CORRECTIONS: Dict[str, str] = {
#     '[0-9\s](\s*[점]\s+)[0-9]': ".",
# }

# def apply_regular_expression_before_convert(sentence):
#     for regex_num in REGEX_NUMBERS_BEFORE_CONVERT:
#         # regexp = re.compile(regex_num)
#         re_iter = re.finditer(regex_num, sentence)
#         for s in re_iter:
#             sentence = sentence[:s.start()] + sentence[s.start():s.end()].replace(s.group(1), txt_to_digit(s.group(1))) + sentence[s.end():]
#     return sentence

# def apply_regular_expression(sentence: str) -> str:
#     for regex_num in REGEX_NUMBERS_AFTER_CONVERT:
#         re_iter = re.finditer(regex_num, sentence)
#         for s in re_iter:
#             sentence = sentence[:s.start()] + sentence[s.start():s.end()].replace(s.group(1), txt_to_digit(s.group(1))) + sentence[s.end():]
#     for regex_text in REGEX_TEXT_CORRECTIONS:
#         re_iter_text = re.finditer(regex_text, sentence)
#         for s in re_iter_text:
#             sentence = sentence[:s.start()] + sentence[s.start():s.end()].replace(s.group(1), REGEX_TEXT_CORRECTIONS[regex_text]) + sentence[s.end():]
#     return sentence

# # def pass_numbers(sentence: str) -> str:
# #     for regex in PASS_NUMBERS:
# #         re_iter = re.finditer(regex, sentence)
# #         for s in re_iter:
# #             sentence = sentence[:s.start()] + sentence[s.start():s.end()].replace(s.group(1), get_txt(s.group(1))) + sentence[s.end():]
# #     return sentence


