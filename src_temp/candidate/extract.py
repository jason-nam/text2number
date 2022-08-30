from typing import List, Tuple
from unicodedata import is_normalized

from .rule import rule_candidate
from .deep_learning import deep_candidate


def candidate_extract(sent: str):
    _, rule_num = rule_candidate(sent, prefix_suffix=True)
    _, deep_num = deep_candidate(sent)

    is_rule_num = False
    is_deep_num = False
    is_both_num = False
    curr_ind = None
    curr_num = ""
    cand_sent = ""
    cand_num = list()
    for ind, char in enumerate(sent):
        if not is_rule_num and rule_num and rule_num[0][1] == ind:
            is_rule_num = True
        elif is_rule_num and rule_num[0][1] + len(rule_num[0][0]) == ind:
            is_rule_num = False
            rule_num.pop(0)

        if not is_deep_num and deep_num and deep_num[0][1] == ind:
            is_deep_num = True
        elif is_deep_num and deep_num[0][1] + len(deep_num[0][0]) == ind:
            is_deep_num = False
            deep_num.pop(0)

        if not is_both_num and is_rule_num and is_deep_num:
            is_both_num = True
            curr_num = curr_num + char
            curr_ind = ind
            cand_sent = cand_sent + "[" + char
        elif is_both_num and is_rule_num and is_deep_num:
            curr_num = curr_num + char
            cand_sent = cand_sent + char
        elif is_both_num and (not is_rule_num or not is_deep_num):
            cand_num.append((curr_num, curr_ind))
            is_both_num = False
            curr_num = ""
            curr_ind = None
            cand_sent = cand_sent + "]" + char
        else:
            cand_sent = cand_sent + char
    
    return cand_sent, cand_num


if __name__ == "__main__":
    None