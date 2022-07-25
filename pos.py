try:
    from konlpy.tag import Mecab
except:
    from eunjeon import Mecab

mecab = Mecab()

def get_pos(txt):
    return mecab.pos(txt)

def get_morphs(txt):
    return mecab.morphs(txt)

if __name__ == "__main__":
    txt = "2번 3 회 추경예산안은 고용 사회안전망 강화와 경기 보강을 위해서."
    print(get_pos(txt))
    
#이번
#백제
#~