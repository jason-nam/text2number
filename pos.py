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
    None