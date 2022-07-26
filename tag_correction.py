import pos
import transform_index

# def num_two_correction(sentence: list) -> list:
#     if sentence.replace(" ",'') =='':
#         return pos.get_pos(sentence)
#     sen_pos = pos.get_pos(sentence)
#     newList =[]
#     place = 0
#     for i in range(len(sen_pos)-1):
#         if sen_pos[i]==('이', 'JKS'):
#             if sen_pos[i+1][1]=='NR':
#                 for a in range(place, len(sentence)):
#                     if sentence[a:a+2]=='이'+sen_pos[i+1][0]:
#                        newList.append(('이', 'NR'))
#                        place = a
#                        break
#             else: newList.append(sen_pos[i])
#         else: newList.append(sen_pos[i])
#     newList.append(sen_pos[len(sen_pos)-1])
#     return newList

UNITS = ["일", "이", "삼", "사", "오", "육", "칠", "팔", "구",]


def subject_case_marker(sentence:str, sentence_pos: list) -> list:
    for pos_ind, pos_key in enumerate(sentence_pos):
        if pos_key[0] in UNITS and pos_key[1] == "JKS" and sentence_pos[pos_ind+1][1] == "NR" and sentence[transform_index.get_txt_ind(sentence, pos_ind)-1] == " ":
            sentence_pos[pos_ind] = (pos_key[0], "NR")
    return sentence_pos


def apply_tag_correction(sentence: str) -> list:
    sentence_pos = pos.get_pos(sentence)
    sentence_pos = subject_case_marker(sentence, sentence_pos)
    return sentence_pos


if __name__ == "__main__":
    txt = "이 사업은 계획이 변경 이천이십 년 사월 십칠일에 나왔다."
    print(apply_tag_correction(txt))
