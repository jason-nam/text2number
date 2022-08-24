from typing import List, Tuple

try:
    from konlpy.tag import Mecab
    mecab = Mecab()
except:
    from eunjeon import Mecab
    mecab = Mecab('C:\\Python39\\Lib\\site-packages\\eunjeon\\data\\mecab-ko-dic-msvc\\mecabrc')


def get_pos(txt: str) -> List[Tuple[str, str]]:
    """
    """
    return mecab.pos(txt)


def get_morphs(txt: str) -> List[str]:
    """
    """
    return mecab.morphs(txt)


if __name__ == "__main__":
    None
