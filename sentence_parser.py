"""
STT
"""

import new_language
import into_digit
import pattern_language
import tag_correction
import month_exception
import text_to_list

# from hanspell import spell_checker
# from kss import split_sentences


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

# def no_space_list(sentences: list) -> list:
#     """remove all spaces in sentences"""

#     no_space_sentences = []
#     for sentence in sentences:
#         no_space_sentences.append(sentence.replace(" ",""))
#     return no_space_sentences

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


def exceptionNR(nr_list: list) -> list:
    """
    
    """

    copy = nr_list
    list_nr_but_no = text_to_list.TextIntoList("exception_nr.txt")
    for ind, each_nr in enumerate(nr_list):
        if each_nr != ():
            for exception in list_nr_but_no:
                if each_nr[0] == exception:
                    null_info = ()
                    copy[ind] = null_info
    return copy

def BringNumber(sentence: str) -> list:
    """
    
    """

    #list1 = tn.checkTwo(sentence)
    list1 = tag_correction.num_two_correction(sentence)
    filtered_nr_list = []
    for a in list1:
        if a[1] == 'NR':
            filtered_nr_list.append(a)
        else:
            b=()
            filtered_nr_list.append(b)
    filtered_nr_list = exceptionNR(filtered_nr_list)
    string_list = []
    str = ''
    for a in filtered_nr_list:
        b = ()
        if a != b:
            str += a[0]
        else:
            if str != '':
                string_list.append(str)
                str = ''
    return string_list

def PutNumber(sentence: str) -> str:
    """
    
    """
    
    #numList = tn.checkTwo(sentence)
    num_list = BringNumber(sentence)
    #print(num_list)
    copy = ''
    result_sentence = ''
    for num in num_list:
        len_copy = len(copy)
        while len_copy <= len(sentence)-1:
            if sentence[len_copy] != num[0]:
                result_sentence += sentence[len_copy]
                len_copy +=1
            else:
                if sentence[len_copy:len_copy+len(num)] == num:
                    result_sentence += into_digit.ToDigit(num)
                    copy = sentence[0:len_copy+len(num)]
                    len_copy = len(sentence)
                else:
                    result_sentence += sentence[len_copy]
                    len_copy +=1
    return result_sentence +sentence[len(copy):]




def main(sentence: str) -> str:
    """worker function"""

    sentence=new_language.apply_dictionary(sentence) # 
    # print('1:',sentence)
    sentence = PutNumber(sentence)
    # print('2:',sentence)
    sentence=pattern_language.apply_regular_expression(sentence) #원문장 정규
    # print('3:',sentence)
    sentence=month_exception.get_month_exception(sentence)
    # print('4:',sentence)
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
print(main("그리고 백이십삼 쪽 스포츠 산업 활성화 지원 증액 부분 두 가지 부분에 대해서 질의하겠습니다 어 우선 이 두 부분은 그 야당 국회의원께서 어 지난 유월 중순에 보도 자료를 내면서 집행률이 영 점 삼 프로 내지는 팔 점 육 프로에 불과하다."))