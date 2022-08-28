from typing import Any, List, Optional, Tuple

# from .rule_util import get_pos, get_text_ind, get_pos_ind
from rule_util import get_pos, get_text_ind, get_pos_ind


class Unit:
    """
    """
    UNITS = ["일", "이", "삼", "사", "오", "육", "칠", "팔", "구"]


class CorrectTag:
    """
    """
    NR_TO_NULL = [
        [('범', 'NNBC'), -1, False, True], [('몇', 'MM'), 1, True, True],
        [("제", "NNBC"), -1, True, True], [("한", "MM"), 1, True, False],
        [("쓰리", "NR"), 1, False, False], [("포", "NR"), 1, False, False],
        [("파이브", "NR"), 1, False, False], [("이런", "NR"), 0, False, False]
    ]
    NULL_TO_NR = [
        [("쪽", "NNB"), -1, False, True], [('인', 'VCP+ETM'), -1, False, True],
        [("당", "XSN"), -1, False, False], [("천", "NR"), -1, True, False]
    ]


class Tag(Unit, CorrectTag):
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
        for ind, pos in enumerate(self.tag_sent):
            for ind, element in enumerate(self.NR_TO_NULL):
                if pos != element[0]:
                    continue
                if (
                    self.tag_sent[ind + element[-3]] != ()
                    and self.tag_sent[ind + element[-3]][1] == "NR"
                    and element[-2]
                    and not self.is_separated(ind, element[-3])
                ):
                    #특정 숫자들만 바꿔야 할 경우 여기다가 추가하면 됨
                    self.tag_sent[ind + element[-3]] = (self.tag_sent[ind + element[-3]][0], 'Null')
                    if element[-1]:
                        at_where = ind + element[-3] * 2
                        while self.tag_sent[at_where][1] == "NR":
                            #특정 숫자들만 바꿔야 할 경우 여기다가 추가하면 됨
                            self.tag_sent[at_where] = (self.tag_sent[at_where][0], "Null")
                elif (
                    self.tag_sent[ind + element[-3]] != ()
                    and self.tag_sent[ind + element[-3]][1] == "NR"
                    and not element[-2]
                ):
                    #특정 숫자들만 바꿔야 할 경우 여기다가 추가하면 됨
                    self.tag_sent[ind + element[-3]] = (self.tag_sent[ind + element[-3]][0], "Null")
                    if element[-1]:
                        at_where = ind + element[-3] * 2
                        while self.tag_sent[at_where][1] == "NR":
                            #특정 숫자들만 바꿔야 할 경우 여기다가 추가하면 됨
                            self.tag_sent[at_where] = (self.tag_sent[at_where][0], "Null")
        return True

    def none_to_num(self) -> bool:
        """
        """
        for ind, element in enumerate(self.NULL_TO_NR):
            for ind, pos in enumerate(sentence_pos):
                if (
                    pos != ()
                    and pos == element[0]
                ):
                    if (
                        self.tag_sent[ind + element[-3]] != ()
                        and self.tag_sent[ind + element[-3]][0][0] in self.UNITS
                    ):
                        if (
                            element[-2]
                            and not self.is_separated(ind, element[-3])
                        ):
                            #특정 숫자들만 바꿔야 할 경우 여기다가 추가하면 됨
                            self.tag_sent[ind + element[-3]] = (self.tag_sent[ind + element[-3]][0], 'NR')
                            if element[-1]:
                                at_where = ind + element[-3] * 2
                                while self.tag_sent[at_where][0] in self.UNITS:
                                    #특정 숫자들만 바꿔야 할 경우 여기다가 추가하면 됨
                                    self.tag_sent[at_where] = (self.tag_sent[at_where][0], 'NR')
                        elif not element[-2]:
                            #특정 숫자들만 바꿔야 할 경우 여기다가 추가하면 됨
                            self.tag_sent[ind + element[-3]] = (self.tag_sent[ind + element[-3]][0], 'NR')
                            if element[-1]:
                                at_where = ind + element[-3] * 2
                                while self.tag_sent[at_where][0] in self.UNITS:
                                    #특정 숫자들만 바꿔야 할 경우 여기다가 추가하면 됨
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
            self.resolve_mecab_version_issue
            and self.none_to_num
            and self.num_to_none
        )


class CandidateSentenceParserInterface:
    """Interface for 'CandidateSentenceParser'"""

    def __init__(self) -> None:
        """Initialize parser."""

    def push_sentence(self, sentence: str) -> bool:
        """Push next sentence."""
        return NotImplemented

    @property
    def sentence_candidate(self) -> str:
        """Get value of current candidate sentence."""
        return NotImplemented

    @property
    def number_candidate(self) -> List[Tuple[str, int]]:
        """Get list values of identified number candidates."""
        return NotImplemented


class CandidateSentenceParser(CandidateSentenceParserInterface):
    """
    """

    def __init__(self) -> None:
        """"""
        super().__init__()
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

    def remove(self) -> None:
        """
        """
        dodge = [
            '하나', '둘', '셋', '넷', '다섯', '여섯', '여덟',
            '아홉', '열', '수십', '수백', '수천', '수만', '수억'
        ]
        for ind, (key, tag) in enumerate(self.curr_tag.tag_sentence):
            if (
                tag == "NR"
                and key in dodge
            ):
                self.curr_tag.set_tag(ind, "Null")

    def find(self) -> bool:
        """
        """
        self.remove()
        batch: str = ""
        batch_ind: Optional[int] = None
        last_tag: Optional[str] = None
        for ind, (key, tag) in enumerate(self.curr_tag.tag_sentence):
            if (
                tag == "NR"
                and last_tag == "NR"
            ):
                if (get_text_ind(self.curr_sent, ind) - get_text_ind(self.curr_sent, ind - 1) == 1):
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

    def parse(self) -> None:
        """
        """
        for num, ind in reversed(self.curr_num):
            self.curr_sent = self.curr_sent[:ind] + "[" + num + "]" + self.curr_sent[ind+len(num):]
            self.num_cand.append((num, ind + len(self.sent_cand)))
        self.sent_cand = self.sent_cand + self.curr_sent

    def push_sentence(self, sent: str) -> bool:
        """
        """
        self.curr_sent = sent
        if (
            not self.curr_tag.sentence_in(sent)
            and not self.find()
        ):
            return False
        self.find()
        self.parse()
        print(self.curr_sent)
        print(self.curr_num)
        self.curr_sent = None
        self.curr_num = []
        return True


if __name__ == "__main__":
    sent_parser = CandidateSentenceParser()

    print(sent_parser.push_sentence("내 나이는 오십이야. 너는 누구니?"))
    print(sent_parser.sent_cand)
    print(sent_parser.number_candidate)
