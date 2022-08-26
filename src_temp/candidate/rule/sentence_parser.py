from typing import Any, List, Optional, Tuple

from .rule_util import get_pos, get_text_ind, get_pos_ind


class Unit:
    """
    """
    UNITS = ["일", "이", "삼", "사", "오", "육", "칠", "팔", "구"]


class CorrectTag:
    """
    """
    NR_TO_NULL = [
        [('범','NNBC'),-1,False,True],[('몇','MM'),1,True,True],
        [("제","NNBC"),-1,True,True],[("한","MM"),1,True,False],
        [("쓰리","NR"),1,False,False],[("포","NR"),1,False,False],
        [("파이브","NR"),1,False,False],[("이런","NR"),0,False,False]
    ]
    NULL_TO_NR = [
        [("쪽","NNB"),-1,False, True],[('인','VCP+ETM'),-1,False,True],
        [("당","XSN"),-1,False,False],[("천","NR"),-1,True,False]
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

    def _is_separated(self, tag_ind: int, dir: int) -> bool:
        """
        """
        if not self.sent:
            return False
        text_ind = get_text_ind(self.sent, tag_ind)
        target_ind = get_text_ind(self.sent, tag_ind + dir)
        return not (
            (text_ind - target_ind) == -1 
            or (text_ind - target_ind) == 1)
    
    def _resolve_mecab_version_issue(self) -> bool:
        """
        """
        if not self.tag_sent:
            return False
        for ind, (key, tag) in enumerate(self.tag_sent[1:-1], start=1):
            if not tag == "NR":
                continue
            else:
                if all(
                    front_back_pos_element in ["NNG", "NNP"] 
                    for front_back_pos_element in [self.tag_sent[ind-1][1], self.tag_sent[ind+1][1]]
                ):
                    self.tag_sent[ind] = (key, "Null")
        return True

    def num_to_none(self):
        """
        """
        for ind,element in enumerate(self.NR_TO_NULL):
            for ind,pos in enumerate(self.pos_sent):
                if pos != () and pos == element[0]:
                    if self.pos_sent[ind+element[-3]]!= () and self.pos_sent[ind+element[-3]][1] =='NR':
                        if element[-2] and not self.is_separated(self.sent, self.pos_sent, ind, element[-3]):
                            #특정 숫자들만 바꿔야 할 경우 여기다가 추가하면 됨
                            self.pos_sent[ind+element[-3]] = (self.pos_sent[ind+element[-3]][0], 'Null')
                            if element[-1]:
                                at_where = ind+element[-3]*2
                                while self.pos_sent[at_where][1] =='NR':
                                    #특정 숫자들만 바꿔야 할 경우 여기다가 추가하면 됨
                                    self.pos_sent[at_where] = (self.pos_sent[at_where][0],'Null')
                        elif not element[-2]:
                            #특정 숫자들만 바꿔야 할 경우 여기다가 추가하면 됨
                            self.pos_sent[ind+element[-3]] = (self.pos_sent[ind+element[-3]][0], 'Null')
                            if element[-1]:
                                at_where = ind+element[-3]*2
                                while self.pos_sent[at_where][1] =='NR':
                                    #특정 숫자들만 바꿔야 할 경우 여기다가 추가하면 됨
                                    self.pos_sent[at_where] = (self.pos_sent[at_where][0],'Null')
        return self.pos_sent                
                
    def none_to_num(self, sentence,sentence_pos):
        """
        """
        for ind, element in enumerate(self.NULL_TO_NR):
            for ind, pos in enumerate(sentence_pos):
                if (
                    pos != () 
                    and pos == element[0]
                ):
                    if (
                        sentence_pos[ind + element[-3]] != () 
                        and sentence_pos[ind + element[-3]][0][0] in self.UNITS
                    ):
                        if (
                            element[-2] 
                            and not self.is_separated(sentence, sentence_pos, ind, element[-3])
                        ):
                            #특정 숫자들만 바꿔야 할 경우 여기다가 추가하면 됨
                            sentence_pos[ind + element[-3]] = (sentence_pos[ind + element[-3]][0], 'NR')
                            if element[-1]:
                                at_where = ind + element[-3] * 2
                                while sentence_pos[at_where][0] in self.UNITS:
                                    #특정 숫자들만 바꿔야 할 경우 여기다가 추가하면 됨
                                    sentence_pos[at_where] = (sentence_pos[at_where][0], 'NR')
                        elif not element[-2]:
                            #특정 숫자들만 바꿔야 할 경우 여기다가 추가하면 됨
                            sentence_pos[ind + element[-3]] = (sentence_pos[ind + element[-3]][0], 'NR')
                            if element[-1]:
                                at_where = ind + element[-3] * 2
                                while sentence_pos[at_where][0] in self.UNITS:
                                    #특정 숫자들만 바꿔야 할 경우 여기다가 추가하면 됨
                                    sentence_pos[at_where] = (sentence_pos[at_where][0], 'NR')
        return sentence_pos   

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

    def sentence_in(self, sent: str) -> bool:
        """
        """
        if self.sent:
            self.all_sent = self.all_sent + self.sent
        if self.tag_sent:
            self.all_tag_sent = self.all_tag_sent.extend(self.tag_sent)
        self.sent = sent
        self.tag_sent = get_pos(sent)

        return (
            self._resolve_mecab_version_issue
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
        self.curr_num: Optional[List[Tuple[str, int]]] = None
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

    def _remove(self) -> None:
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
                self.curr_tag.tag_sentence[ind] = (key, "Null")

    def _find(self) -> bool:
        """
        """
        # sentence_pos = correct_tags(sentence, sentence_pos)
        # pos_list = []

        # for pos in sentence_pos:
        #     if pos[1] != 'NR':
        #         null_info=()
        #         pos_list.append(null_info)
        #     else:
        #         pos_list.append(pos)

        self._remove()

        # pos_list = exceptionNR(pos_list)
        # string_list = []
        # str = ""
        # NR_index_in_sentence = 0

        batch: str = ""
        batch_ind: Optional[int] = None
        last_tag: Optional[str] = None
        for ind, (key, tag) in enumerate(self.curr_tag.tag_sentence):
            # b = ()
            if (
                tag == "NR"
                and ind == (len(self.curr_tag.tag_sentence) - 1)
            ):
                batch = batch + key
                batch_ind = ind if not batch else None
                self.curr_num.append((batch, get_text_ind(self.curr_sent, batch_ind)))
                batch = ""
            elif (
                not tag == "NR"
                and batch
            ):
                self.curr_num.append((batch, get_text_ind(self.curr_sent, batch_ind)))
                batch = ""
            elif (
                tag == "NR"
                and ind != 0
                and last_tag == "NR"
                and get_text_ind(self.curr_sent, ind) - get_text_ind(self.curr_sent, ind - 1) != 1
            ):
                self.curr_num.append((batch, get_text_ind(self.curr_sent, batch_ind)))
                batch = key
                batch_ind = ind
                


            # if tag == "NR":
            #     if self.curr_tag[ind - 1] != ():
            #         txt_ind = get_text_ind(self.curr_sent, ind)
            #         txt_ind2 = get_text_ind(self.curr_sent, ind-1)
            #         if txt_ind2 == None:
            #             difference = 1
            #         else:   
            #             difference = txt_ind - txt_ind2 

            #         if difference != 1:
            #             self.curr_num.append((str, get_text_ind(self.curr_sent, ind)))
            #             str = self.curr_tag[ind][0]
            #         else:
            #             if str == '':
            #                 NR_index_in_sentence = ind
            #             str += key
            #     else:
            #         if str == '':
            #             NR_index_in_sentence = ind
            #         str += key
            # else:
            #     if str != '':
            #         self.curr_num.append((str, get_text_ind(self.curr_sent, ind)))
            #         str = ''
            # if (
            #     self.curr_tag[ind] != () 
            #     and ind == len(self.curr_tag) - 1
            # ):
            #     self.curr_num.append((str, get_text_ind(self.curr_sent, ind)))  
        return True

    def _parse(self) -> None:
        """
        """
        if not self.curr_num:
            return
        for num, ind in reversed(self.curr_num):
            self.curr_sent = self.curr_sent[:ind] + "[" + num + "]" + self.curr_sent[ind+len(num):]
        self.cand_sent = self.cand_sent + self.curr_sent

    def push_sentence(self, sent: str) -> bool:
        """
        """
        self.curr_sent = sent
        if (
            not self.curr_tag.sentence_in(sent)
            and not self._find()
        ):
            return False
        self._parse()
        self.curr_sent = None
        self.curr_num = None
        return True


if __name__ == "__main__":
    sent_parser = CandidateSentenceParser()
    
    sent_parser.push_sentence("")
    print(sent_parser.sent_cand)
    print(sent_parser.number_candidate)