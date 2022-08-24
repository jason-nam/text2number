"""
Test the ``text_to_num`` library.
"""
from unittest import TestCase, main
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src_temp.candidate import rule_candidate, split


class TestCandidateExtractFromSentence(TestCase):
    def test_rule_split(self):
        sent1 = "네 지금 의원님께서 말씀 주신 대로 현재 어린이집 회계 등 운영 실태 조사를 진행 중에 있습니다 칠월까지인데요."
        self.assertEqual(list(split(sent1)), ["네 지금 의원님께서 말씀 주신 대로 현재 어린이집 회계 등 운영 실태 조사를 ", "진행 중에 있습니다 칠월까지인데요."])

    def test_rule_candidate(self):
        self.assertEqual()

    def test_deep_candidate(self):
        self.assertEqual()

    def test_candidate_extract(self):
        self.assertEqual()

if __name__ == "__main__":
    main()

    