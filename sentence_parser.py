#with 문장분리기
from ast import Num
from doctest import OutputChecker
from re import M
from eunjeon import Mecab
import json

#from numpy import _2Tuple
import exceptions.new_language as ud
from hanspell import spell_checker
import text_to_num as tn
from kss import split_sentences
import exceptions.pattern_language as re
import exceptions.tag_correction as tag_correction

m = Mecab()
"""
with open("3CS01_2137901_20200629_01.json",'r', encoding="UTF-8") as json_file:
    a = json.load(json_file)

toJSON = []
b= a["document"]["utterance"]
"""
#list1 은 utterance모음
list1 = []

"""
for sent in b:
    list1.append(sent["form"])
"""
#list2 는 다 띄워쓰기, list3는 다 붙인것 (utterance모음집에서)
def space_all_list(list1):    
    list2 = []
    for utt in list1:
        a = str(utt)
        a = a.replace(' ','')
        filtered = ''
        for word in a:
            filtered = filtered + word + ' '
        list2.append(filtered)
    return list2

def no_space_list(list1):
    list3 = []
    for i in list1:
        temp = []
        for b in i:
            temp.append(b.replace(" ",""))
        list3.append(temp)
    return list3
#print(list3)

#workigng은 list1,2,3중에서 어떤 걸로 형태소 분석해서 수사들을 추출하는지

def split_list(list1):
    s_list = []
    for i in list1:
        a = split_sentences(i)
        s_list.append(a)
    return s_list
#print(split_list(["안녕하세요. 제 이름은 누구누구입니다.","그래서 어떻게 하실 생각이신가요? 저는 궁금하네요"]))
#print(split_list(["안녕하세요. 제 이름은 누구누구입니다.","그래서 어떻게 하실 생각이신가요? 저는 궁금하네","제이 항에 선거법 제오 조 육사시미 제일 차관의 주최 행사 제이 사당"]))
#working = list1

working = split_list(list1)

#list4는 문장분리기를 통해 forms에서 문장을 나누고 한 forms를 list형태로 묶어서 나누어주었다.
def cut_line_list(list1):
    list4 = []
    ppp=0
    for a in list1:
        #split_sentences return []
        output = split_sentences(a)
        #toJSON[ppp]["Split Sentence"] = split_sentences(a)
        list4.append(output)
        ppp +=1
    return list4

#print(cut_line_list(list1))

def show_pos(sentence):
    a = m.pos(sentence)
    return a
#print(list4)
#이번 사건에서 2번 사건에서
#str인 문장을 넣어서 여기서 숫자들만 가져오는 함수
def bring_number(sentence):
    #list1 = tn.checkTwo(sentence)
    list1 = tag_correction.num_two_correction(sentence)
    f = []
    for a in list1:
        if a[1] == 'NR':
            f.append(a)
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


#수사리스트에서 쓸수있는걸로만 바꿔주는거
###########################################################(이게 실제로 convert하는 마지막 단계!!!!!!!)
#실제로 대입하는 함수 return하는 값은 수사를 아라비아 숫자로 변환하여 반환한다.
def put_number(sentence):
    #numList = tn.checkTwo(sentence)
    numList = bring_number(sentence)

    #print(numList)
    copy = ''
    new = ''
    #string일부 가져오는법 [a:b] a에서 b-1위치까지 가져온다.
    #a is an index value
    for num in numList:
        a = len(copy)
        while a <= len(sentence)-1:
            if sentence[a] != num[0]:
                new += sentence[a]
                a +=1
            else:
                if sentence[a:a+len(num)] == num:
                    new += tn.get(num)
                    copy = sentence[0:a+len(num)]
                    a = len(sentence)
                else:
                    new += sentence[a]
                    a +=1
    return new +sentence[len(copy):]

"""
filter = [] 
for a in working:
    temp = []
    for aa in a:
        b=ud.apply(aa)
        c=re.apply_dictionary(put_number(b))
        temp.append(c)
    filter.append(temp)
filter = no_space_list(filter)
filter1=[]
for a in filter:
    temp =[]
    for aa in a:
        b =spell_checker.check(u''+put_number(aa))
        c = b.checked
        temp.append(c)
    #print(b.checked)
    filter1.append(temp)

filter2 = space_all_list(filter1)
filter3 = []
for a in filter2:
    c = put_number(a)
    c = c.replace(" ",'')
    c=spell_checker.check(u''+c)
    filter3.append(c.checked)

for each in list1:
    a ={}
    a["form"] = each
    toJSON.append(a)
#print(toJSON)
for i in range(len(list1)):
    for aa in filter1[i]:
        toJSON[i]["convert"]=(filter1[i])
    toJSON[i]["number"] = []
    for aa in working[i]:
        toJSON[i]["number"] += bring_number(aa)
    for aa in filter[i]:
        toJSON[i]["number"] += bring_number(aa)
    numList = []
    #그냥 toJSON[i]["number"]에서 직접하거나 "number"바로 아래줄에 바로 "digit을 넣어도 되었네"
    for a in (working[i]):
        for aa in bring_number(a):
            if aa != '':
                numList.append(put_number(aa))
    for a in filter[i]:
        for aa in bring_number(a):
            if aa != '':
                numList.append(put_number(aa))
    
    
    toJSON[i]["digit"] = numList
    
out_file3 = open('7201111final.json', 'w', encoding = 'utf-8')
json.dump(toJSON, out_file3, indent = 4, sort_keys=False, ensure_ascii=False)
out_file3.close()
"""

#print(bring_number(b))

###############################이런경우는 프로를 퍼센트로 바꾸고 점을 다시 바꿔준다음에 다시 퍼센트를 프로로!!] #n점n프로 꼴로~~!!
#print(put_number("네 보통 이제 저 방금 말씀하신 것처럼 이 이제 모태펀드에서 문화계정 이렇게 두면 주로 이제 영화나 이런 쪽에 많이 투자를 하지 않습니까?"))
#print(put_number("그리고 백이십삼 쪽 스포츠 산업 활성화 지원 증액 부분 두 가지 부분에 대해서 질의하겠습니다 어 우선 이 두 부분은 그 야당 국회의원께서 어 지난 유월 중순에 보도 자료를 내면서 집행률이 영 점 삼 프로 내지는 팔 점 육 프로에 불과하다."))
#index로 ~찾고 없앤다음에 변환한 후에 그 위치에 다시 끼어 넣는다.
#print(m.pos("그리고 백이십삼 쪽 스포츠 산업 활성화 지원 증액 부분 두 가지 부분에 대해서 질의하겠습니다 어 우선 이 두 부분은 그 야당 국회의원께서 어 지난 유월 중순에 보도 자료를 내면서 집행률이 영 점 삼 프로 내지는 팔 점 육 프로에 불과하다."))
#print(spacing("안녕하세요 정육점에서 맛있는 음식을 만들고 있습니다."))

def main(sentence: str) -> str:
    sentence=ud.apply_dictionary(sentence)
    sentence=re.apply_regular_expression(put_number(sentence))
    temp_list = [sentence]
    temp_list = split_list(temp_list)
    temp_list = no_space_list(temp_list)
    filter1=[]
    for a in temp_list:
        temp =[]
        for aa in a:
            d=ud.apply_dictionary(aa)
            c=re.apply_regular_expression(put_number(d))
            d =spell_checker.check(u''+put_number(c))
            e = d.checked
            temp.append(e)
        #print(b.checked)
        filter1.append(temp)
    for i in range(len(temp_list)):
        str = ''
        for aa in filter1[i]:
            str += aa
        return str