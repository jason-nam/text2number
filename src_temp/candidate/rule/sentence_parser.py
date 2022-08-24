from typing import List, Optional

class CandidateSentenceParserInterface:
    """Interface for 'CandidateSentenceParser'"""

    def __init__(self) -> None:
        """Initialize parser."""

    @property
    def candidate_sentence(self) -> str:
        """Get value of current candidate sentence."""
        return NotImplemented


class CandidateSentenceParser(CandidateSentenceParserInterface):
    """
    """

    def __init__(self) -> None:
        """"""
        super().__init__()
        self.cand_sent: str = ""

    @property
    def candidate_sentence(self) -> str:
        return self.cand_sent