from typing import Any, Iterator, List, Sequence, Tuple, Union, Optional

from .rule_util import get_pos, get_text_ind
from .sentence_parser import (
    CandidateSentenceParser,
    CandidateSentenceParserInterface
)

NOMINATIVE_KEY: List[str] = ["이", "을", "를", "가", "은", "는"]
NOMINATIVE_TAG: List[str] = ["JKS", "JKC", "JX", "JKO" ] #JKG (?)

def split(sentence: str) -> Iterator[str]:
    """
    """
    sentence_start_index = 0
    sentence_end_index = 0
    for pos_index, pos_element in enumerate(get_pos(sentence)):
        if (
            any(nominative_case_pos_key == pos_element[0] 
                for nominative_case_pos_key in NOMINATIVE_KEY) 
            and any(nominative_case_pos_tag == pos_element[1] 
                for nominative_case_pos_tag in NOMINATIVE_TAG)
        ):
            sentence_end_index = get_text_ind(sentence, pos_index) + 2
            yield sentence[sentence_start_index:sentence_end_index]
            sentence_start_index = sentence_end_index
    yield sentence[sentence_start_index:]


def rule_candidate(
    sentence: str
) -> str:
    """
    """
    sent_parser: CandidateSentenceParserInterface = CandidateSentenceParser()
    for _ in split(sentence):
        pass
    return