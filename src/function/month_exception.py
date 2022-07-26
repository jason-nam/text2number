from util import pos, transform_index
from typing import Dict

MONTHS: Dict[str, str] = {
    "일월": "1월",
    "이월": "2월",
    "삼월": "3월",
    "사월": "4월",
    "오월": "5월",
    "육월": "6월",
    "유월": "6월",
    "칠월": "7월",
    "팔월": "8월",
    "구월": "9월",
    "십월": "10월",
    "시월": "10월",
    "십일월": "11월",
    "십이월": "12월",
}

EXCEPTION_TAGS = ["J", "V", "N", "SN"]

EXCEPTION_KEYS = ["말경"]


def get_month_exception(txt: str) -> str:
    if not any(month in txt for month in MONTHS):
        return txt
    txt_pos = pos.get_pos(txt)
    months_count = 0
    for month in MONTHS:
        for ind, key in enumerate(txt_pos):
            try:
                if key[0] == month and any(txt_pos[ind+1][1].startswith(exception_tag) for exception_tag in EXCEPTION_TAGS):
                    txt_ind =  transform_index.get_txt_ind(txt, ind+months_count)
                    txt = txt[:txt_ind] + txt[txt_ind:txt_ind+len(MONTHS[month])].replace(month, MONTHS[month]) + txt[txt_ind+len(MONTHS[month]):]
                    months_count += 1
                elif key[0] == month and any(txt_pos[ind+1][0].startswith(exception_key) for exception_key in EXCEPTION_KEYS):
                    txt_ind = transform_index.get_txt_ind(txt, ind+months_count)
                    txt = txt[:txt_ind] + txt[txt_ind:txt_ind+len(MONTHS[month])].replace(month, MONTHS[month]) + txt[txt_ind+len(MONTHS[month]):]
                    months_count += 1
            except:
                pass
    return txt

if __name__ == "__main__":
    
    txt = '그 겨울이 지나 이월 말경 다시 학교로 가 졸업식을 치렀다.'
    # print(pos.get_pos(txt))
    print(get_month_exception(txt))

    txt = '기상청에서는 올 이월에도 꽃샘추위가 몇 차례 찾아올 것이라고 전망하였다'
    # print(pos.get_pos(txt))
    print(get_month_exception(txt))

    txt = '저희 회사는 이월에 이월합니다.'
    # print(pos.get_pos(txt))
    print(get_month_exception(txt))

    txt = '오늘은 이월 30일 입니다.'
    # print(pos.get_pos(txt))
    print(get_month_exception(txt))

    txt = '오월이 찾아왔습니다.'
    # print(pos.get_pos(txt))
    print(get_month_exception(txt))
