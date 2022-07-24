import new_language
import text_to_num
import pattern_language
import tag_correction
import month_exception

from hanspell import spell_checker
from kss import split_sentences


# def space_all_list(list1):    
#     """list2 는 다 띄워쓰기, list3는 다 붙인것 (utterance모음집에서)"""
#     list2 = []
#     for utt in list1:
#         a = str(utt)
#         a = a.replace(' ','')
#         filtered = ''
#         for word in a:
#             filtered = filtered + word + ' '
#         list2.append(filtered)
#     return list2

def no_space_list(sentences: list) -> list:
    """remove all spaces in sentences"""

    no_space_sentences = []
    for sentence in sentences:
        no_space_sentences.append(sentence.replace(" ",""))
    return no_space_sentences

# list4는 문장분리기를 통해 forms에서 문장을 나누고 한 forms를 list형태로 묶어서 나누어주었다.
# def cut_line_list(list1):
#     list4 = []
#     ppp=0
#     for a in list1:
#         #split_sentences return []
#         output = split_sentences(a)
#         #toJSON[ppp]["Split Sentence"] = split_sentences(a)
#         list4.append(output)
#         ppp +=1
#     return list4


def bring_number(sentence: str) -> list:
    """문장을 넣어서 여기서 숫자들만 가져오는 함수"""

    list1 = tag_correction.num_two_correction(sentence)
    f = []
    for a in list1:
        if a[1] == 'NR':
            if a[0] == '조':
                b=()
                f.append(b)
            else: f.append(a)
        else:
            b=()
            f.append(b)
    string_list = []
    str = ''
    for a in f:
        b = ()
        if a != b:
            str += a[0]
        else:
            if str != '':
                string_list.append(str)
                str = ''
    return string_list


def put_number(sentence: str) -> str:
    """
    수사리스트에서 쓸수있는걸로만 바꿔주는거
    (이게 실제로 convert하는 마지막 단계!!!!!!!)
    실제로 대입하는 함수 return하는 값은 수사를 아라비아 숫자로 변환하여 반환한다.
    """

    num_list = bring_number(sentence)
    copy = ''
    new = ''
    #string일부 가져오는법 [a:b] a에서 b-1위치까지 가져온다.
    #a is an index value
    for num in num_list:
        len_copy = len(copy)
        while len_copy <= len(sentence)-1:
            if sentence[len_copy] != num[0]:
                new += sentence[len_copy]
                len_copy +=1
            else:
                if sentence[len_copy:len_copy+len(num)] == num:
                    new += text_to_num.get(num)
                    copy = sentence[0:len_copy+len(num)]
                    len_copy = len(sentence)
                else:
                    new += sentence[len_copy]
                    len_copy +=1
    return new +sentence[len(copy):]


def main(sentence: str) -> str:
    """worker function"""

    sentence=new_language.apply_dictionary(sentence) # 
    print('1:',sentence)
    sentence = put_number(sentence)
    print('2:',sentence)
    sentence=pattern_language.apply_regular_expression(sentence) #원문장 정규
    print('3:',sentence)
    sentence=month_exception.get_month_exception(sentence)
    print('4:',sentence)
    # sentence_list = split_sentences(sentence) # kss
    # print('5:',sentence_list)
    # sentence_list = no_space_list(sentence_list) #원문장 띄어쓰기 제거
    # print('6:',sentence_list)
    # transformed_sentence = ''
    # for single_sentence in sentence_list:
    #     print('7:',single_sentence)
    #     spell_check_sentence =spell_checker.check(u''+put_number(new_language.apply_dictionary(single_sentence)))
    #     transformed_sentence += spell_check_sentence.checked + " "
    # return transformed_sentence[:-1]
    return sentence

print(main("정부는 예산에서 육조칠천억 원을 추가한다는 발표를 했습니다."))
print(main("제육 조 제이십사 항을 참고바랍니다. 성원이 되었으므로 제삼백칠십구 회 국회임시회 제일 차 문화체육관광위원회를 개의하겠습니다."))
print(main("성원이 되었으므로 제삼백칠십구 회 국회임시회 제일 차 문화체육관광위원회를 개의하겠습니다."))
print(main("제육 조 제이십사 항을 참고바랍니다."))
print(main('저희 회사는 이월에 이월합니다.'))
# print(main("그리고 백이십삼 쪽 스포츠 산업 활성화 지원 증액 부분 두 가지 부분에 대해서 질의하겠습니다 어 우선 이 두 부분은 그 야당 국회의원께서 어 지난 유월 중순에 보도 자료를 내면서 집행률이 영 점 삼 프로 내지는 팔 점 육 프로에 불과하다."))