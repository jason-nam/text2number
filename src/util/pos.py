try:
    from konlpy.tag import Mecab
except:
    from eunjeon import Mecab

mecab = Mecab()
# print(mecab.pos("허리나 요충사업원 "))

# mecab = Mecab('C:\\Python39\\Lib\\site-packages\\eunjeon\\data\\mecab-ko-dic-msvc\\mecabrc')
# print(mecab.pos("허리나 요충사업원 "))

def get_pos(txt):
    return mecab.pos(txt)

def get_morphs(txt):
    return mecab.morphs(txt)

if __name__ == "__main__":
    # txt = "2번 3 회 추경예산안은 고용 사회안전망 강화와 경기 보강을 위해서."
    # print(get_pos(txt))

    # txt = "나는 코로나 일구에 감염됬었어"
    # print(get_pos(txt))

    # txt = "나는 이번 유일 사일에 본 시험에서 영점 사점을 받았어"
    # print(get_pos(txt))

    txt = "내 전화번호는 공일공 팔육사육 오오오일"
    print(get_pos(txt))

    print(get_pos("우리 제일 법안심사 소위원회는 지난 사월 이십팔 일 총 팔십한 건의 법률안을 심사하여 한 건은 수정안으로 채택하고 스물일곱 건은 통합 조정하여 두 건의 대안으로 제안하기로 의결하였습니다."))
