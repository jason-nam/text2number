from typing import List, Optional, Tuple

from .rule_util import get_pos, get_text_ind, get_pos_ind


class Unit:
    """
    """
    UNITS = ["일", "이", "삼", "사", "오", "육", "칠", "팔", "구"]


class Tag:
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


class CorrectTags(Unit, Tag):
    """
    """

    def __init__(self) -> None:
        """"""
        self.sent: Optional[str] = None 
        self.pos_sent: Optional[List[Tuple[str, str]]] = None

    def is_separated(self, pos_ind: int, dir: int) -> bool:
        """
        """
        if not self.sent:
            return False
        text_ind = get_text_ind(self.sent, self.pos_sent, pos_ind)
        target_ind = get_text_ind(self.sent, self.pos_sent, pos_ind + dir)
        return not (
            (text_ind - target_ind) == -1 
            or (text_ind - target_ind) == 1)
    
    def resolve_mecab_version_issues(self) -> bool:
        """
        """
        if not self.pos_sent:
            return False
        for ind, (key, tag) in enumerate(self.pos_sent[1:-1].items(), start=1):
            if not tag == "NR":
                continue
            else:
                if all(
                    front_back_pos_element in ["NNG", "NNP"] 
                    for front_back_pos_element in [self.pos_sent[ind-1][1], self.pos_sent[ind+1][1]]
                ):
                    self.pos_sent[ind] = (key, "Null")
        return True

    def nr_to_none(self):
        """
        """
        for ind,element in enumerate(self.NR_TO_NULL):
            for ind,pos in enumerate(sentence_pos):
                if pos != () and pos == element[0]:
                    if sentence_pos[ind+element[-3]]!= () and sentence_pos[ind+element[-3]][1] =='NR':
                        if element[-2] and not self.is_separated(self.sent, sentence_pos, ind, element[-3]):
                            #특정 숫자들만 바꿔야 할 경우 여기다가 추가하면 됨
                            sentence_pos[ind+element[-3]] = (sentence_pos[ind+element[-3]][0], 'Null')
                            if element[-1]:
                                at_where = ind+element[-3]*2
                                while sentence_pos[at_where][1] =='NR':
                                    #특정 숫자들만 바꿔야 할 경우 여기다가 추가하면 됨
                                    sentence_pos[at_where] = (sentence_pos[at_where][0],'Null')
                        elif not element[-2]:
                            #특정 숫자들만 바꿔야 할 경우 여기다가 추가하면 됨
                            sentence_pos[ind+element[-3]] = (sentence_pos[ind+element[-3]][0], 'Null')
                            if element[-1]:
                                at_where = ind+element[-3]*2
                                while sentence_pos[at_where][1] =='NR':
                                    #특정 숫자들만 바꿔야 할 경우 여기다가 추가하면 됨
                                    sentence_pos[at_where] = (sentence_pos[at_where][0],'Null')
        return sentence_pos                
                
    def none_to_nr(self, sentence,sentence_pos):
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

    def correct_tags(self, sentence, pos_sent):
        """
        """
        pos_sent = self.resolve_mecab_version_issues(
            self.nr_to_none(
                sentence, 
                self.none_to_nr(
                    sentence, 
                    pos_sent
                )
            )
        )
        return pos_sent


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
        self.sent_tag = CorrectTags()
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

    def find(sentence: str, sentence_pos: List[Tuple[str, str]]) -> bool:
        """
        """
        sentence_pos = correct_tags(sentence, sentence_pos)
        pos_list = []

        for pos in sentence_pos:
            if pos[1] != 'NR':
                null_info=()
                pos_list.append(null_info)
            else:
                pos_list.append(pos)

        pos_list = exceptionNR(pos_list)
        string_list = []
        str = ""
        NR_index_in_sentence = 0

        for ind, a in enumerate(pos_list):
            b = ()
            if a != b:
                if pos_list[ind - 1] != b:
                    txt_ind = get_txt_ind_impr(sentence, ind)
                    txt_ind2 = get_txt_ind_impr(sentence, ind-1)
                    if txt_ind2 == None:
                        difference = 1
                    else:   
                        difference = txt_ind - txt_ind2 

                    if difference != 1:
                        string_list.append((str, get_txt_ind_impr(sentence, NR_index_in_sentence)))
                        str = pos_list[ind][0]
                        NR_index_in_sentence = ind
                    else:
                        if str == '':
                            NR_index_in_sentence = ind
                        str += a[0]
                else:
                    if str == '':
                        NR_index_in_sentence = ind
                    str += a[0]
            else:
                if str != '':
                    string_list.append((str, get_txt_ind_impr(sentence, NR_index_in_sentence)))
                    str = ''
            if (
                pos_list[ind] != b 
                and ind == len(pos_list) - 1
            ):
                string_list.append((str, get_txt_ind_impr(sentence, NR_index_in_sentence)))  
        return string_list 

    def parse(self) -> None:
        """
        """
        if not self.curr_num:
            return
        for num, ind in reversed(self.curr_num):
            self.curr_sent = "".join(
                self.curr_sent[:ind], 
                "[", num, "]",
                self.curr_sent[ind+len(num):]
            )

    def push_sentence(self, sentence: str) -> bool:
        """
        """
        self.curr_sent = sentence
        if not self.find(self.curr_sent, get_pos(self.curr_sent)):
            return False

        self.parse()
        self.cand_sent = self.cand_sent + self.curr_sent

        self.curr_sent = None
        self.curr_num = None
        return True


if __name__ == "__main__":
    sent_parser = CandidateSentenceParser()
    
    sent_parser.push_sentence("")
    print(sent_parser.sent_cand)
    print(sent_parser.number_candidate)