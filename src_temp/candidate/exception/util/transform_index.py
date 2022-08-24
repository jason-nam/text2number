from typing import List

from .pos import get_morphs

def get_text_ind(sentence: str, ind_pos: int) -> int:
    """
    """
    ind_in_sentence = 0
    sent_morph = get_morphs(sentence)
    sub_sent = sentence[ind_in_sentence:]

    if ind_pos > len(sent_morph):
        raise ValueError("invalid index position: {}".format(repr(ind_pos)))

    for ind, morph in enumerate(sent_morph):
        while sub_sent[0] == " ":
            ind_in_sentence += 1
            sub_sent = sentence[ind_in_sentence]
        if ind == ind_pos:
            break
        else:
            ind_in_sentence += len(morph)
            sub_sent = sentence[ind_in_sentence:]
    return ind_in_sentence


def get_pos_ind(sentence: str, ind_sent: int) -> int:
    """
    """
    pos_char_count = 0
    word_char_count = 0
    ind_pos = 0
    sent_morph = get_morphs(sentence)
    sub_sent = sentence[:ind_sent]

    if ind_sent > len(sentence):
        raise ValueError("invalid index position: {}".format(repr(ind_sent)))

    for c in sub_sent:
        word_char_count += 1 if c != " " else None
    for ind, morph in enumerate(sent_morph):
        for _ in morph:
            if pos_char_count == word_char_count:
                ind_pos = ind
            pos_char_count += 1
    return ind_pos


if __name__ == "__main__":
    None