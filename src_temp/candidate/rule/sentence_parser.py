from typing import Any, List, Optional, Tuple, Dict
import re, os, json

from .rule_util import get_pos, get_text_ind, get_pos_ind

_dir = os.path.dirname(os.path.abspath(__file__))
prefix_suffix_path = os.path.join(_dir, "./prefix_suffix")

with open(os.path.join(prefix_suffix_path, "prefix.json"), "r", encoding="utf-8") as file:
    prefix = json.load(file)

with open(os.path.join(prefix_suffix_path, "suffix.json"), "r", encoding="utf-8") as file:
    suffix = json.load(file)


class Unit:
    """
    """
    UNITS: List[str] = ["일", "이", "삼", "사", "오", "육", "칠", "팔", "구"]


class TagCorrectionInfo:
    """
    """
    NR_TO_NULL: List[Dict[str, Any]] = [
        {"tag": ('범', 'NNBC'), "dir": -1, "remove_space": False, "continue_nr_check": True},
        {"tag": ('몇', 'MM'), "dir": 1, "remove_space": True, "continue_nr_check": True},
        {"tag": ('제', 'NNBC'), "dir": -1, "remove_space": True, "continue_nr_check": True},
        {"tag": ('한', 'MM'), "dir": 1, "remove_space": True, "continue_nr_check": False},
        {"tag": ('쓰리', 'NR'), "dir": 1, "remove_space": False, "continue_nr_check": False},
        {"tag": ('포', 'NR'), "dir": 1, "remove_space": False, "continue_nr_check": False},
        {"tag": ('파이브', 'NR'), "dir": 1, "remove_space": False, "continue_nr_check": False},
        {"tag": ('이런', 'NR'), "dir": 0, "remove_space": False, "continue_nr_check": False},
    ]

    NULL_TO_NR: List[Dict[str, Any]] = [
        {"tag": ('쪽', 'NNB'), "dir": -1, "remove_space": False, "continue_nr_check": True},
        {"tag": ('인', 'VCP+ETM'), "dir": -1, "remove_space": False, "continue_nr_check": True},
        {"tag": ('당', 'XSN'), "dir": -1, "remove_space": False, "continue_nr_check": False},
        {"tag": ('천', 'NR'), "dir": -1, "remove_space": True, "continue_nr_check": False},
    ]


class Tag(Unit, TagCorrectionInfo):
    """
    """

    def __init__(self) -> None:
        """"""
        self.sent: Optional[str] = None
        self.tag_sent: Optional[List[Tuple[str, str]]] = None
        self.all_sent = ""
        self.all_tag_sent = []

    @property
    def tag_sentence(self) -> List[Tuple[str, str]]:
        return self.tag_sent

    def is_separated(self, tag_ind: int, dir: int) -> bool:
        """
        """
        if not self.sent:
            return False
        text_ind = get_text_ind(self.sent, tag_ind)
        target_ind = get_text_ind(self.sent, tag_ind + dir)
        return not (
            (text_ind - target_ind) == -1
            or (text_ind - target_ind) == 1)

    def resolve_mecab_version_issue(self) -> bool:
        """
        """
        if not self.tag_sent:
            return False
        for ind, (key, tag) in enumerate(self.tag_sent[1:-1], start=1):
            if not tag == "NR":
                continue
            if all(
                fb_tag in ["NNG", "NNP"]
                for fb_tag in [self.tag_sent[ind-1][1], self.tag_sent[ind+1][1]]
            ):
                self.tag_sent[ind] = (key, "Null")
        return True

    def num_to_none(self) -> bool:
        """
        """
        for ind, (key, tag) in enumerate(self.tag_sent):
            for ind, item in enumerate(self.NR_TO_NULL):
                if (key, tag) != item["tag"]:
                    continue
                if (
                    ind + item["dir"] < len(self.tag_sent)
                    and self.tag_sent[ind + item["dir"]][1] == "NR"
                    and item["remove_space"]
                    and not self.is_separated(ind, item["dir"])
                ):
                    self.tag_sent[ind + item["dir"]] = (self.tag_sent[ind + item["dir"]][0], 'Null')
                    if item["continue_nr_check"]:
                        at_where = ind + item["dir"] * 2
                        while self.tag_sent[at_where][1] == "NR":
                            self.tag_sent[at_where] = (self.tag_sent[at_where][0], "Null")
                elif (
                    ind + item["dir"] < len(self.tag_sent)
                    and self.tag_sent[ind + item["dir"]][1] == "NR"
                    and not item["remove_space"]
                ):
                    self.tag_sent[ind + item["dir"]] = (self.tag_sent[ind + item["dir"]][0], "Null")
                    if item["continue_nr_check"]:
                        at_where = ind + item["dir"] * 2
                        while self.tag_sent[at_where][1] == "NR":
                            self.tag_sent[at_where] = (self.tag_sent[at_where][0], "Null")
        return True

    def none_to_num(self) -> bool:
        """
        """
        for ind, (key, tag) in enumerate(self.tag_sent):
            for ind, item in enumerate(self.NULL_TO_NR):
                if (key, tag) != item["tag"]:
                    continue
                if (
                    ind + item["dir"] < len(self.tag_sent)
                    and self.tag_sent[ind + item["dir"]][0] in self.UNITS
                    and item["remove_space"]
                    and not self.is_separated(ind, item["dir"])
                ):
                    self.tag_sent[ind + item["dir"]] = (self.tag_sent[ind + item["dir"]][0], 'NR')
                    if item["continue_nr_check"]:
                        at_where = ind + item["dir"] * 2
                        while self.tag_sent[at_where][0] in self.UNITS:
                            self.tag_sent[at_where] = (self.tag_sent[at_where][0], 'NR')
                elif (
                    ind + item["dir"] < len(self.tag_sent)
                    and self.tag_sent[ind + item["dir"]][0] in self.UNITS
                    and not item["remove_space"]
                ):
                    self.tag_sent[ind + item["dir"]] = (self.tag_sent[ind + item["dir"]][0], 'NR')
                    if item["continue_nr_check"]:
                        at_where = ind + item["dir"] * 2
                        while self.tag_sent[at_where][0] in self.UNITS:
                            self.tag_sent[at_where] = (self.tag_sent[at_where][0], 'NR')
        return True

    def set_key(self, ind: int, key: str) -> bool:
        if (
            not key
            or ind < 0
            or ind > len(self.tag_sent)
        ):
            return False
        self.tag_sent[ind] = (key, self.tag_sent[ind][1])
        return True

    def set_tag(self, ind: int, tag: str) -> bool:
        if (
            not tag
            or ind < 0
            or ind > len(self.tag_sent)
        ):
            return False
        self.tag_sent[ind] = (self.tag_sent[ind][0], tag)
        return True

    def is_empty(self) -> bool:
        return not self.tag_sent

    def sentence_in(self, sent: str) -> bool:
        """
        """
        if self.sent:
            self.all_sent = self.all_sent + self.sent
        if self.tag_sent:
            self.all_tag_sent.extend(self.tag_sent)
        self.sent = sent
        self.tag_sent = get_pos(sent)
        return (
            self.resolve_mecab_version_issue()
            and self.none_to_num()
            and self.num_to_none())


class CandidateSentenceParser:
    """
    """

    def __init__(self) -> None:
        """"""
        self.sent: str = ""
        self.curr_sent: Optional[str] = None
        self.curr_num: List[Tuple[str, int]] = []
        self.curr_tag = Tag()
        self.sent_cand: str = ""
        self.num_cand: List[Tuple[str, int]] = []

    @property
    def sentence_candidate(self) -> str:
        """"""
        return self.sent_cand

    @property
    def number_candidate(self) -> List[str]:
        """"""
        return self.num_cand

    def remove_tag(self) -> None:
        """
        """
        bad_key = [
            '하나', '둘', '셋', '넷', '다섯', '여섯', '여덟',
            '아홉', '열', '수십', '수백', '수천', '수만', '수억'
        ]
        for ind, (key, tag) in enumerate(self.curr_tag.tag_sentence):
            if (
                tag == "NR"
                and key in bad_key
            ):
                self.curr_tag.set_tag(ind, "Null")

    def remove_num(self) -> None:
        """
        """
        bad_num = ["삼삼오오", "열사"]
        for num, _ in self.curr_num:
            if num in bad_num:
                self.curr_num.remove(num)

    def find(self) -> bool:
        """
        """
        self.remove_tag()
        batch: str = ""
        batch_ind: Optional[int] = None
        last_tag: Optional[str] = None
        for ind, (key, tag) in enumerate(self.curr_tag.tag_sentence):
            if (
                tag == "NR"
                and last_tag == "NR"
            ):
                if (get_text_ind(self.curr_sent, ind) - get_text_ind(self.curr_sent, ind - 1) == len(self.curr_tag.tag_sentence[ind - 1][0])):
                    batch = batch + key
                else:
                    self.curr_num.append((batch, get_text_ind(self.curr_sent, batch_ind)))
                    batch = key
                    batch_ind = ind
            elif (
                tag == "NR"
                and last_tag != "NR"
            ):
                batch = key
                batch_ind = ind
            elif (
                tag != "NR"
                and last_tag == "NR"
            ):
                self.curr_num.append((batch, get_text_ind(self.curr_sent, batch_ind)))
                batch = ""
            elif (
                tag != "NR"
                and last_tag != "NR"
            ):
                continue
            if (
                tag == "NR"
                and ind == (len(self.curr_tag.tag_sentence) - 1)
            ):
                self.curr_num.append((batch, get_text_ind(self.curr_sent, batch_ind)))
            last_tag = tag
        return True

    def filter_prefix_suffix(self) -> None:
        filtered_num = list()
        for num, ind in self.curr_num:
            remove_num = True
            for p in prefix:
                if self.curr_sent[:ind].strip().endswith(p):
                    remove_num = False
            for s in suffix:
                if self.curr_sent[ind + len(num):].strip().startswith(s):
                    remove_num = False
            if not remove_num:
                filtered_num.append((num, ind))
        self.curr_num = filtered_num

    def parse(self) -> None:
        """
        """
        rev_curr_num = list()
        for num, ind in reversed(self.curr_num):
            self.curr_sent = self.curr_sent[:ind] + "[" + num + "]" + self.curr_sent[ind + len(num):]
            rev_curr_num.append((num, ind + len(re.sub("[\[\]]", "", self.sent_cand))))
        self.sent_cand = self.sent_cand + self.curr_sent
        self.num_cand.extend(reversed(rev_curr_num))

    def push_sentence(self, sent: str, prefix_suffix: bool) -> bool:
        """
        """
        self.sent = self.sent + sent
        self.curr_sent = sent
        if (
            not self.curr_tag.sentence_in(sent)
            and not self.find()
        ):
            return False
        self.find()
        if prefix_suffix:
            self.filter_prefix_suffix()
        self.remove_num()
        self.parse()
        self.curr_sent = None
        self.curr_num = []
        return True


if __name__ == "__main__":
    sent_parser = CandidateSentenceParser()

    print(sent_parser.push_sentence("내 나이는 오십이야. 너는 누구니?"))
    print(sent_parser.sent_cand)
    print(sent_parser.number_candidate)
