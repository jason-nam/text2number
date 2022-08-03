from util import *

def get_txt_ind(txt: str, ind_pos: int) -> int:
    txt_morph = get_morphs(txt)
    txt_word = txt.split()
    pos_char_count = 0
    word_char_count = 0
    ind_txt = 0
    for morph in txt_morph[:ind_pos]:
        pos_char_count += len(morph)
    txt_word = txt.split()
    word_char_count = 0
    for ind, word in enumerate(txt_word):
        for char in word:
            word_char_count += 1
            if word_char_count == pos_char_count:
                ind_txt = pos_char_count+ind +1
                break
    return ind_txt

def get_txt_ind_impr(sentence, ind_pos):
    txt_morph = get_morphs(sentence)
    ind_in_sentence =0
    copy = sentence[ind_in_sentence:]
    #print(txt_morph)
    for ind, morph in enumerate(txt_morph):
        while copy[0] ==' ':
            ind_in_sentence += 1
            copy = sentence[ind_in_sentence]
        if ind == ind_pos:
            return ind_in_sentence
        else:
            ind_in_sentence += len(morph)
            copy = sentence[ind_in_sentence:]

def get_pos_ind(txt: str, ind_txt: int) -> int:
    txt_morph = get_morphs(txt)
    txt_word = txt[:ind_txt]
    pos_char_count = 0
    word_char_count = 0
    ind_pos = 0

    for c in txt_word:
        if c != " ":
            word_char_count += 1
    for ind, morph in enumerate(txt_morph):
        for char in morph:
            if pos_char_count == word_char_count:
                ind_pos = ind
            pos_char_count += 1
    return ind_pos


if __name__ == "__main__":
    txt = '오월이 찾아왔습니다.'
    print("TXT INDEX:", txt[0], 0)
    print("POS INDEX:", get_pos(txt)[get_pos_ind(txt, 0)], get_pos_ind(txt, 0))

    print(get_txt_ind(txt,0))

    print("TXT INDEX RETURN:", txt[get_txt_ind(txt, get_pos_ind(txt, 0))], get_txt_ind(txt, get_pos_ind(txt, 0)))