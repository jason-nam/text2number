import re
from typing import Dict, List


class NumberRegexExpression:
    INIT = "(?:^|\s)"
    UNIT = "([영일이삼사오육칠팔구]{1})"
    MTENS = "([십백천]{1})"
    MTENTHOUSANDS = "([만억조경해]{1})"


class RegularRegexExpression:
    TIME_REGEX = [
        "(?:^|\s)([영일이삼사오육칠팔구십백천만억]{1,})\s{0,}년",
        "(?:^|\s)([영일이삼사오육유칠팔구십시]{1,2})\s{0,}월[^하했할]", # "...사 월에는..."
        "(?:^|\s)[영일이삼사오육유칠팔구십시]{1,2}\s{0,}월\s{0,}([일이삼사오육칠팔구십]{1,})\s{0,}일[^일]", # "...구 월 이십일..."
        "(?:^|\s)([영일이삼사오육칠팔구십백천만억]{1,})\s{0,}년\s{0,}([일이삼사오육칠팔구십]{1,})\s{0,}일[^일]", # "...이천이십이년 이십일일..."
    ]

    MATH_REGEX = [
        '(?:^|\s)([영일이삼사오육칠팔구십백천만억조해경]{1,})\s{0,}점\s{0,}([영일이삼사오육칠팔구]{1,})\s{0,}(?:프로|점|퍼센트|그람|킬로|톤)', # "...구점 일 프로..."
        '(?:^|\s)([영일이삼사오육칠팔구십백천만억조해경]{1,})\s{0,}분의\s{0,}([영일이삼사오육칠팔구십백천만억조해경]{1,})',
    ]

    COUNT_REGEX = [
        '(?:^|\s)제([영일이삼사오육칠팔구십백천만억조해경]{1,})\s{0,}(?:항|조|목|차관|조항|항목|관|회|차|법안심사)', # "...제 삼백칠십 항..."
        '(?:^|\s)전과\s{0,}([영일이삼사오육칠팔구십백천]{1,})\s{0,}범', # "...전과 구..."
        '(?:^|\s)([영일이삼사오육륙칠팔구십백천]{1,})\s{0,}다시\s{0,}([영일이삼사오육륙칠팔구십백천]{1,})',
    ]

    ID_NUMBER_REGEX = [
        '(?:^|\s)([공영일이삼사오육칠팔구]{2,3})\s{0,}([공영일이삼사오육칠팔구]{3,4})\s{0,}([공영일이삼사오육칠팔구]{4})', # "...공일공 이이이이 일일일일..."
        '(?:^|\s)([공영일이삼사오육칠팔구]{3})\s{0,}(?:다시|에)\s{0,}([공영일이삼사오육칠팔구]{2,4})\s{0,}(?:다시|에)\s{0,}([공영일이삼사오육칠팔구]{4,5})', # 사업자 번호
    ]

    REGULAR_REGEX = TIME_REGEX.copy()
    REGULAR_REGEX.extend(MATH_REGEX)
    REGULAR_REGEX.extend(COUNT_REGEX)
    REGULAR_REGEX.extend(ID_NUMBER_REGEX)


class MiscRegexExpression:
    MISC_REGEX: Dict[str, str] = {
        '[0-9](\s{0,}점\s{0,})[0-9]': ".", # "...6 점 5..."
        '[0-9](\s{0,}다시\s{0,})[0-9]': "-", # "...6 다시 5..."
    }


class RegexParser(NumberRegexExpression, RegularRegexExpression, MiscRegexExpression):
    def __init__(self, sent):
        self.sent = sent
        self.num = list()

    def regular_regex(self) -> str:
        for regex_num in self.REGULAR_REGEX:
            re_iter = re.finditer(regex_num, self.sent)
            for s in re_iter:
                for i in reversed(range(1, len(s.groups())+1)):
                    start = s.span(i)[0]
                    end = s.span(i)[1]

                    # self.regex_sent = (
                    #     self.sent[:start]
                    #     + self.sent[start:end].replace(s.group(i), "[{}]".format(s.group(i))) 
                    #     + self.regex_sent[end:]
                    # )
                    self.num.append((s.group(i), start))
        return self.num

    def misc_regex(self, sent) -> str:
        for regex_text in self.MISC_REGEX:
            re_iter_text = re.finditer(regex_text, sent)
            for s in re_iter_text:
                for i in reversed(range(1, len(s.groups())+1)):
                    start = s.span(i)[0]
                    end = s.span(i)[1]
                    sent = (
                        sent[:start]
                        + sent[start:end].replace(s.group(i), self.MISC_REGEX[regex_text])
                        + sent[end:]
                    )
        return sent

if __name__ == "__main__":
    None


