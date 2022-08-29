from typing import List, Tuple

from rule import rule_candidate
from deep_learning import deep_candidate

def candidate_extract(sent: str) -> Tuple[str, List[Tuple[str, int]]]:
    rule_sent, rule_num = rule_candidate(sent)
    deep_sent, deep_num = deep_candidate(sent)

    print(rule_sent)
    print(rule_num)
    print(deep_sent)
    print(deep_num)
    
    return


if __name__ == "__main__":
    print(candidate_extract("삼백육십오일 동안 무엇을 했는가"))