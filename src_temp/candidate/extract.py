from typing import List, Tuple

from .rule import rule_candidate
from .deep_learning import deep_candidate

def candidate_extract(sent: str) -> Tuple[str, List[Tuple[str, int]]]:
    rule_sent, rule_num = rule_candidate(sent)
    deep_sent, deep_num = deep_candidate(sent)
    return