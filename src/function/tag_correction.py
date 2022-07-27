from util import *


UNITS = ["일", "이", "삼", "사", "오", "육", "칠", "팔", "구",]

def subject_case_marker(sentence:str, sentence_pos: list) -> list:
    for pos_ind, pos_key in enumerate(sentence_pos):
        try:
            if pos_key[0] in UNITS and pos_key[1] == "JKS" and sentence_pos[pos_ind+1][1] == "NR" and sentence[get_txt_ind(sentence, pos_ind)-1] == " ":
                sentence_pos[pos_ind] = (pos_key[0], "NR")
        except:
            pass
    return sentence_pos


def fixing_NR_after_MM(sentence_pos: list) -> list:
    filtered_pos = sentence_pos
    for i in range(len(sentence_pos)-1):
        if sentence_pos[i] != () and sentence_pos[i+1] != ():
            if sentence_pos[i] == ('몇','MM') and sentence_pos[i+1][1]=='NR':
                filtered_pos[i+1] = (filtered_pos[i+1][0],'NONO')
    return filtered_pos

def fixing_NR_after_NNB(sentence_pos):
    filtered_pos = sentence_pos
    for ind in  range(1,len(sentence_pos)):
        if sentence_pos[ind] != () and sentence_pos[ind-1] != ():
            if sentence_pos[ind] == ('쪽','NNB') and sentence_pos[ind-1][1] == 'NNG':
                if sentence_pos[ind-1][0] in UNITS:
                    filtered_pos[ind-1] = (filtered_pos[ind-1][0],'NR')
    return filtered_pos   

def fixing_per_person(sentence_pos):
    filtered_pos = sentence_pos
    for ind in  range(2,len(sentence_pos)):
        if sentence_pos[ind] != () and sentence_pos[ind-1] != () and sentence_pos[ind-2] != ():
            if sentence_pos[ind] == ('당','NNG') and sentence_pos[ind-2][1] !='NR' and sentence_pos[ind-1]==('인','VCP+ETM'):
                if sentence_pos[ind-2][0] in UNITS:
                    filtered_pos[ind-2] = (filtered_pos[ind-2][0],'NR')
    for ind in  range(1,len(sentence_pos)):
        if sentence_pos[ind] != () and sentence_pos[ind-1] != ():
            if sentence_pos[ind] == ('당','XSN') and sentence_pos[ind-1][1] == 'NNG':
                if sentence_pos[ind-1][0][0] in UNITS:
                    filtered_pos[ind-1] = (filtered_pos[ind-1][0][0],'NR')
                    filtered_pos[ind] = (filtered_pos[ind-1][0][1:]+filtered_pos[ind][0],'XSN')
    return filtered_pos

def apply_tag_correction(sentence: str) -> list:
    sentence_pos = get_pos(sentence)
    sentence_pos = subject_case_marker(sentence, sentence_pos)
    sentence_pos = fixing_NR_after_MM(sentence_pos)
    sentence_pos = fixing_NR_after_NNB(sentence_pos)
    sentence_pos = fixing_per_person(sentence_pos)
    return sentence_pos


if __name__ == "__main__":
    txt = "이 사업은 계획이 변경 이천이십 년 사월 십칠일에 나왔다."
    print(apply_tag_correction("나는 팔 쪽에서 가져왔다."))
    print(apply_tag_correction(txt))
