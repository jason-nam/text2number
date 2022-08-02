try:
    from konlpy.tag import Mecab
except:
    from eunjeon import Mecab

# mecab = Mecab()
# print(mecab.pos("허리나 요충사업원 "))

mecab = Mecab('C:\\Python39\\Lib\\site-packages\\eunjeon\\data\\mecab-ko-dic-msvc\\mecabrc')
# print(mecab.pos("허리나 요충사업원 "))

mecab = Mecab()

def get_pos(txt):
    return mecab.pos(txt)

def get_morphs(txt):
    return mecab.morphs(txt)

if __name__ == "__main__":
    txt = "그래서 사급 판정 뒤에 일박 팔박 구일 동안 유럽 여행을 가시고"
    print(get_pos(txt))
    print(mecab.nouns(txt))