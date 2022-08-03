UNITS = ["일", "이", "삼", "사", "오", "육", "칠", "팔", "구"]
#띄워쓰기 없어야하는가 -> 없어야하는경우 True, 상관없는 경우 False
#[해당하는 특정포스, 앞인지뒤인지, 띄워쓰기 없어야하는가,NRcheck계속가야하는지]
list_nr_to_null = [[('범','NNBC'),-1,False,True],[('몇','MM'),1,True,True],[("제","NNBC"),-1,True,True],[("한","MM"),1,True,False],[("쓰리","NR"),1,False,False],[("포","NR"),1,False,False],[("파이브","NR"),1,False,False]]
list_not_to_nr = [[("쪽","NNB"),-1,False, True],[('인','VCP+ETM'),-1,False,True],[("당","XSN"),-1,False,False],[("천","NR"),-1,True,False]]

def get_text_ind(sentence,sentence_pos,ind_pos):
    txt_morph = sentence_pos
    ind_in_sentence =0
    copy = sentence[ind_in_sentence:]
    for ind, morph in enumerate(txt_morph):
        while copy[0] == ' ':
            ind_in_sentence += 1
            copy = sentence[ind_in_sentence]
        if ind == ind_pos:
            return ind_in_sentence
        else:
            ind_in_sentence += len(morph[0])
            copy = sentence[ind_in_sentence:]

def resolve_mecab_version_issues(sentence_pos):
    for sentence_pos_index, sentence_pos_element in enumerate(sentence_pos[1:-1], start=1):
        if not sentence_pos_element[1] == "NR":
            continue
        else:
            if all(front_back_pos_element in ["NNG", "NNP"] for front_back_pos_element in [sentence_pos[sentence_pos_index-1][1], sentence_pos[sentence_pos_index+1][1]]):
                sentence_pos[sentence_pos_index] = (sentence_pos_element[0], "Null")
    return sentence_pos

#("문장",[형태소분석],24(특정형태소 위치), 어느쪽확인해야하는지 1 or -1)
def SpaceBetween(sentence,sentence_pos, ind_pos, FrontOrBack):
    ind_of_pos_in_sentence = get_text_ind(sentence,sentence_pos,ind_pos)
    ind_of_possible_NR_in_sentence = get_text_ind(sentence,sentence_pos,ind_pos+FrontOrBack)
    if (ind_of_pos_in_sentence - ind_of_possible_NR_in_sentence) == -1 or(ind_of_pos_in_sentence - ind_of_possible_NR_in_sentence) == 1:
        return False
    return True

def FilterNR_toNone(sentence, sentence_pos):
    """
    changing NR to NULL
    """
    for ind,element in enumerate(list_nr_to_null):
        for ind,pos in enumerate(sentence_pos):
            if pos != () and pos == element[0]:
                if sentence_pos[ind+element[-3]]!= () and sentence_pos[ind+element[-3]][1] =='NR':
                    if element[-2] and not SpaceBetween(sentence,sentence_pos, ind, element[-3]):
                        #특정 숫자들만 바꿔야 할 경우 여기다가 추가하면 됨
                        sentence_pos[ind+element[-3]] = (sentence_pos[ind+element[-3]][0], 'Null')
                        if element[-1]:
                            at_where = ind+element[-3]*2
                            while sentence_pos[at_where][1] =='NR':
                                #특정 숫자들만 바꿔야 할 경우 여기다가 추가하면 됨
                                sentence_pos[at_where] = (sentence_pos[at_where][0],'Null')
                    elif not element[-2]:
                        #특정 숫자들만 바꿔야 할 경우 여기다가 추가하면 됨
                        sentence_pos[ind+element[-3]] = (sentence_pos[ind+element[-3]][0], 'Null')
                        if element[-1]:
                            at_where = ind+element[-3]*2
                            while sentence_pos[at_where][1] =='NR':
                                #특정 숫자들만 바꿔야 할 경우 여기다가 추가하면 됨
                                sentence_pos[at_where] = (sentence_pos[at_where][0],'Null')
    return sentence_pos                
            
def FilterNone_toNR(sentence,sentence_pos):
    """
    changing non_NR to NR
    """
    for ind,element in enumerate(list_not_to_nr):
        for ind,pos in enumerate(sentence_pos):
            if pos != () and pos == element[0]:
                if sentence_pos[ind+element[-3]]!= () and sentence_pos[ind+element[-3]][0][0] in UNITS:
                    if element[-2] and not SpaceBetween(sentence,sentence_pos, ind, element[-3]):
                        #특정 숫자들만 바꿔야 할 경우 여기다가 추가하면 됨
                        sentence_pos[ind+element[-3]] = (sentence_pos[ind+element[-3]][0], 'NR')
                        if element[-1]:
                            at_where = ind+element[-3]*2
                            while sentence_pos[at_where][0] in UNITS:
                                #특정 숫자들만 바꿔야 할 경우 여기다가 추가하면 됨
                                sentence_pos[at_where] = (sentence_pos[at_where][0],'NR')
                    elif not element[-2]:
                        #특정 숫자들만 바꿔야 할 경우 여기다가 추가하면 됨
                        sentence_pos[ind+element[-3]] = (sentence_pos[ind+element[-3]][0], 'NR')
                        if element[-1]:
                            at_where = ind+element[-3]*2
                            while sentence_pos[at_where][0] in UNITS:
                                #특정 숫자들만 바꿔야 할 경우 여기다가 추가하면 됨
                                sentence_pos[at_where] = (sentence_pos[at_where][0],'NR')
    return sentence_pos   

def correct_tags(sentence, sentence_pos):
    sentence_pos = resolve_mecab_version_issues(FilterNone_toNR(sentence, FilterNR_toNone(sentence, sentence_pos)))
    return sentence_pos

if __name__ == '__main__':
    #print(str(list_nr_to_null))
    temp = list_nr_to_null[0][0:len(list_nr_to_null[0])-1]
    temp = str(temp)
    temp = temp[1:len(temp)-1]
    #print(temp)
    #print(m.pos("그 식당은 십 인당 몇장까지 사용가능한가요? 몇십만명이 그곳에 방문했습니다."))
    sentence = "사람이 천이십년도에 여행을 갔다. 그 식당은 오인당 몇장까지 사용가능한가요? 몇십만명이 그곳에 방문했습니다. 그 사람은 전과 십이범이다. 육쪽입니까? 확인해보세요 보시면 이십삼쪽에 나와있다고 하네요. 그러면 백제문화유산인데 그래도 되나요?"
    #sentence = "사람이 천이십년도에 여행갔다. 사람 이천이십년도에 여행갔다."
    #print(FilterNR_toNone(sentence,m.pos(sentence)))
    # print(FilterNone_toNR(sentence,FilterNR_toNone(sentence,m.pos(sentence))))

# from util import *

# UNITS = ["일", "이", "삼", "사", "오", "육", "칠", "팔", "구",]

# NR_NULL = "NR_NULL"

# def get_text_ind(sentence, ind_pos):
#     txt_morph = get_morphs(sentence)
#     ind_in_sentence = 0
#     copy = sentence[ind_in_sentence:]
#     for ind, morph in enumerate(txt_morph):
#         while copy[0] ==' ':
#             ind_in_sentence += 1
#             copy = sentence[ind_in_sentence]
#         if ind == ind_pos:
#             return ind_in_sentence
#         else:
#             ind_in_sentence += len(morph)
#             copy = sentence[ind_in_sentence:]

# def resolve_mecab_version_issues(sentence_pos):
#     for sentence_pos_index, sentence_pos_element in enumerate(sentence_pos[1:-1], start=1):
#         if not sentence_pos_element[1] == "NR":
#             continue
#         else:
#             if all(front_back_pos_element in ["NNG", "NNP"] for front_back_pos_element in [sentence_pos[sentence_pos_index-1][1], sentence_pos[sentence_pos_index+1][1]]):
#                 sentence_pos[sentence_pos_index] = (sentence_pos_element[0], "NR_NULL")
#     return sentence_pos

# def subject_case_marker(sentence:str, sentence_pos: list) -> list:
#     for pos_ind, pos_key in enumerate(sentence_pos):
#         try:
#             if pos_key[0] in UNITS and pos_key[1] == "JKS" and sentence_pos[pos_ind+1][1] == "NR" and sentence[get_txt_ind(sentence, pos_ind)-1] == " ":
#                 sentence_pos[pos_ind] = (pos_key[0], "NR")
#         except:
#             pass
#     return sentence_pos


# def fixing_NR_after_MM(sentence_pos: list) -> list:
#     filtered_pos = sentence_pos
#     if "몇" not in str(sentence_pos):
#         return sentence_pos
#     for i in range(len(sentence_pos)-1):
#         if sentence_pos[i] != () and sentence_pos[i+1] != ():
#             if sentence_pos[i] == ('몇','MM') and sentence_pos[i+1][1]=='NR':
#                 filtered_pos[i+1] = (filtered_pos[i+1][0],'NR_NULL')
#     return filtered_pos

# def fixing_NR_after_NNB(sentence_pos):
#     filtered_pos = sentence_pos
#     for ind in  range(1,len(sentence_pos)):
#         if sentence_pos[ind] != () and sentence_pos[ind-1] != ():
#             if sentence_pos[ind] == ('쪽','NNB') and sentence_pos[ind-1][1] == 'NNG':
#                 if sentence_pos[ind-1][0] in UNITS:
#                     filtered_pos[ind-1] = (filtered_pos[ind-1][0],'NR')
#     return filtered_pos   

# def fixing_BaekJe(sentence, sentence_pos):
#     filtered_pos = sentence_pos
#     for ind in  range(1,len(sentence_pos)):
#         if sentence_pos[ind] != () and sentence_pos[ind-1] != ():
#             if sentence_pos[ind][0][0] == '제' and sentence_pos[ind-1] == ('백','NR') and  not sentence[get_text_ind(sentence,ind)-1] == " ":
#                 filtered_pos[ind-1] = (filtered_pos[ind-1][0],'NR_NULL')
#     return filtered_pos

# def fixing_Baek_Bum(sentence, sentence_pos):
#     filtered_pos = sentence_pos
#     for ind in  range(1,len(sentence_pos)):
#         if sentence_pos[ind] != () and sentence_pos[ind-1] != ():
#             if sentence_pos[ind] == ('범', "NNBC"):
#                 for index_temp in range(ind-1,0, -1):
#                     if(sentence_pos[index_temp][1] == 'NR'):
#                         filtered_pos[index_temp] = (filtered_pos[index_temp][0],'NR_NULL')
#                         continue
#                     else:
#                         break
#     return filtered_pos

# def fixing_Han_Il(sentence, sentence_pos):
#     filtered_pos = sentence_pos
#     for ind in  range(1,len(sentence_pos)):
#         if sentence_pos[ind] != () and sentence_pos[ind-1] != ():
#             if sentence_pos[ind] ==  ('일','NR') and sentence_pos[ind-1][0] == '한' and  not sentence[get_text_ind(sentence,ind)-1] == " ":
#                 filtered_pos[ind] = (filtered_pos[ind][0],'NR_NULL')
#     return filtered_pos

# def fixing_per_person(sentence_pos):
#     filtered_pos = sentence_pos
#     for ind in  range(2,len(sentence_pos)):
#         if sentence_pos[ind] != () and sentence_pos[ind-1] != () and sentence_pos[ind-2] != ():
#             if sentence_pos[ind] == ('당','NNG') and sentence_pos[ind-2][1] !='NR' and sentence_pos[ind-1]==('인','VCP+ETM'):
#                 if sentence_pos[ind-2][0] in UNITS:
#                     filtered_pos[ind-2] = (filtered_pos[ind-2][0],'NR')
#     for ind in  range(1,len(sentence_pos)):
#         if sentence_pos[ind] != () and sentence_pos[ind-1] != ():
#             if sentence_pos[ind] == ('당','XSN') and sentence_pos[ind-1][1] == 'NNG':
#                 if sentence_pos[ind-1][0][0] in UNITS:
#                     filtered_pos[ind-1] = (filtered_pos[ind-1][0][0],'NR')
#                     filtered_pos[ind] = (filtered_pos[ind-1][0][1:]+filtered_pos[ind][0],'XSN')
#     return filtered_pos

# def fixing_TTE(sentence, sentence_pos):
#     filtered_pos = sentence_pos
#     for ind in range(1,len(sentence_pos)):
#         if sentence_pos[ind]!=() and sentence_pos[ind-1]!=():
#             if sentence_pos[ind] == ('때','NNG') and sentence_pos[ind-1][1] == 'NR':
#                 for reverse_ind in range(ind-2,0,-1):
#                     if sentence_pos[reverse_ind][1] == 'NR' and sentence[get_text_ind[sentence, reverse_ind]+1] != ' ':
#                         filtered_pos[reverse_ind][1] = 'NR_NULL'
#                     else:
#                         break
#                 filtered_pos[ind-1] = (sentence_pos[ind-1][0],'NR_NULL')
#     return filtered_pos

# def fixing_2_bun(sentence, sentence_pos):
#     filter_pos = sentence_pos
#     if len(sentence_pos) >= 2 and sentence_pos[0] == ('이','NR') and sentence_pos[1] == ('번', "NNBC") and sentence[1] != ' ':
#         filter_pos[0] = ('이번','right_now')
#         del filter_pos[1]
#     return filter_pos

# def apply_tag_correction(sentence: str, sentence_pos: list) -> list:
#     sentence_pos = resolve_mecab_version_issues(sentence_pos)
#     sentence_pos = subject_case_marker(sentence, sentence_pos)
#     sentence_pos = fixing_NR_after_MM(sentence_pos)
#     sentence_pos = fixing_NR_after_NNB(sentence_pos)
#     sentence_pos = fixing_per_person(sentence_pos)
#     sentence_pos = fixing_BaekJe(sentence, sentence_pos)
#     sentence_pos = fixing_Baek_Bum(sentence, sentence_pos)
#     sentence_pos = fixing_TTE(sentence, sentence_pos)
#     sentence_pos = fixing_Han_Il(sentence, sentence_pos)
#     sentence_pos = fixing_2_bun(sentence, sentence_pos)
    
#     return sentence_pos


# if __name__ == "__main__":
#     txt = "이 사업은 계획이 변경 이천이십 년 사월 십칠일에 나왔다."
#     txt = "사업체를 가지고 있어."
#     print(apply_tag_correction("나는 팔 쪽에서 가져왔다."))
#     print(apply_tag_correction(txt))
