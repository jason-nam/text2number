try:
    from konlpy.tag import Mecab
    mecab = Mecab()
except:
    from eunjeon import Mecab
    mecab = Mecab('C:\\Python39\\Lib\\site-packages\\eunjeon\\data\\mecab-ko-dic-msvc\\mecabrc')


def get_pos(txt):
    return mecab.pos(txt)


def get_morphs(txt):
    return mecab.morphs(txt)


if __name__ == "__main__":
    None
