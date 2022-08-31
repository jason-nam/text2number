import logging
from typing import final

from .candidate import candidate_extract
from .text_to_num import text2num
from .exception import (
    RegexParser
)

MULTIPLIERS = {
    1: "",
    1_0000: "만",
    1_0000_0000: "억",
    1_0000_0000_0000: "조",
    1_0000_0000_0000_0000: "경",
    1_0000_0000_0000_0000_0000: "해",
}


def remove_duplicate(final_num):
    for list_ind, (num, ind) in enumerate(final_num):
        if list_ind == len(final_num) - 1:
            break
        ind_ahead = final_num[list_ind + 1][1]
        if ind_ahead < ind + len(num):
            final_num.pop(list_ind + 1)
    return final_num


def arabic_to_hangeul_parser(final_num):
    relaxed = False
    hangeul_num_list = list()
    for num, _ in final_num:
        try:
            arabic_num = text2num(num, "kr", relaxed)
            hangeul_num = ""
            for mult in reversed(MULTIPLIERS):
                mtenthousands = (arabic_num // mult) % 1_0000
                if mtenthousands != 0 and mtenthousands != 1:
                    hangeul_num = hangeul_num + str(mtenthousands) + MULTIPLIERS[mult]
            hangeul_num_list.append(hangeul_num)
        except:
            hangeul_num_list.append(num)
    return hangeul_num_list


def main(sent: str):
    regex_parser = RegexParser(sent)

    i, cand_num = candidate_extract(sent)
    cand_num = sorted(cand_num, key=lambda num: num[1])
    regex_num = regex_parser.regular_regex()
    regex_num = sorted(regex_num, key=lambda num: num[1])

    final_num = list()
    while cand_num or regex_num:
        if cand_num:
            cnum, cind = cand_num[0][0], cand_num[0][1]
        else: 
            final_num.extend(regex_num)
            break
        if regex_num:
            rnum, rind = regex_num[0][0], regex_num[0][1]
        else:
            final_num.extend(cand_num)
            break

        if cnum == rnum and cind == rind:
            final_num.append((cnum, cind))
            cand_num.pop(0)
            regex_num.pop(0)
        elif cnum != rnum and cind == rind:
            final_num.append((max(cnum, rnum), cind))
            cand_num.pop(0)
            regex_num.pop(0)
        elif (
            cind > rind 
            and cind < rind + len(rnum)
            and cind + len(cnum) >= rind + len(rnum)
        ):
            final_num.append((rnum + cnum[len(rnum):], rind))
            cand_num.pop(0)
            regex_num.pop(0)
        elif (
            rind > cind 
            and rind < cind + len(cnum)
            and rind + len(rnum) >= cind + len(cnum)
        ):
            final_num.append((cnum + rnum[len(cnum):], cind))
            cand_num.pop(0)
            regex_num.pop(0)
        elif (
            cind > rind 
            and cind < rind + len(rnum)
            and cind + len(cnum) < rind + len(rnum)
        ):
            final_num.append((rnum + cnum[len(rnum):] + rnum[len(rnum + cnum[len(rnum):]):], rind))
            cand_num.pop(0)
            regex_num.pop(0)
        elif (
            rind > cind 
            and rind < cind + len(cnum)
            and rind + len(rnum) < cind + len(cnum)
        ):
            final_num.append((cnum + rnum[len(cnum):] + cnum[len(cnum + rnum[len(cnum):]):], cind))
            cand_num.pop(0)
            regex_num.pop(0)
        else:
            final_num.append((cnum, cind)) if cind < rind else final_num.append((rnum, rind))
            cand_num.pop(0) if cind < rind else regex_num.pop(0)

    final_num = remove_duplicate(sorted(final_num, key=lambda num: num[1]))
    hangeul_num = arabic_to_hangeul_parser(final_num)

    for num_id, (num, ind) in reversed((list(enumerate(final_num)))):
        sent = sent[:ind] + hangeul_num[num_id] + sent[ind + len(num):]
    return regex_parser.misc_regex(sent)

# if __name__ == "__main__":
#     print(main("그리고 문화체육관광부장관님 그 문체부는 저희 지금 이천이십 년 삼 차 추경으로 한 삼천사백억 정도를 결정하셨고 올해 그 문체부 예산 육 조 사천팔백억의 약 삼 프로에 달하는 어 천팔백억 정도를 어~ 구조조정하면서 추경안을 마련한 것인데요."))