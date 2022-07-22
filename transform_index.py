import pos

def get_txt_ind(txt, ind_pos):
    txt_morph = pos.get_morphs(txt)
    txt_word = txt.split()
    pos_char_count = 0
    word_char_count = 0
    ind_txt = None
    for morph in txt_morph[:ind_pos]:
        pos_char_count += len(morph)
    txt_word = txt.split()
    word_char_count = 0
    for ind, word in enumerate(txt_word):
        for char in word:
            word_char_count += 1
            if word_char_count == pos_char_count:
                ind_txt = pos_char_count+ind+1
    return ind_txt

def get_pos_ind(txt, ind_txt):
    txt_morph = pos.get_morphs(txt)
    txt_word = txt[:ind_txt+1].split()
    pos_char_count = 0
    word_char_count = 0
    ind_pos = None
    word_char_count = ind_txt-len(txt_word)+1
    for ind, morph in enumerate(txt_morph):
        for char in morph:
            if pos_char_count == word_char_count:
                ind_pos = ind
            pos_char_count += 1
    return ind_pos


if __name__ == "__main__":
    txt = "그리고 백이십삼 쪽 스포츠 산업 활성화 지원 증액 부분 두 가지 부분에 대해서 질의하겠습니다 어 우선 이 두 부분은 그 야당 국회의원께서 어 지난 유월 중순에 보도 자료를 내면서 집행률이 영 점 삼 프로 내지는 팔 점 육 프로에 불과하다."
    print("TXT INDEX:", txt[15], 15)
    print("POS INDEX:", pos.get_pos(txt)[get_pos_ind(txt, 15)], get_pos_ind(txt, 15))
    print("TXT INDEX RETURN:", txt[get_txt_ind(txt, get_pos_ind(txt, 15))], get_txt_ind(txt, get_pos_ind(txt, 15)))