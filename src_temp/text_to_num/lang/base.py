from typing import Dict, Optional, Set, Tuple

class Language:
    """Base class for language object."""

    MULTIPLIERS: Dict[str, int]
    UNITS: Dict[str, int]
    STENS: Dict[str, int]
    TEN: Dict[str, int]
    MTENS: Dict[str, int]
    MTENS_WSTENS: Set[str]
    HUNDRED: Dict[str, int]
    MHUNDREDS: Dict[str, int] = {}
    THOUSAND: Dict[str, int]
    MTHOUSANDS: Dict[str, int]
    NUMBERS: Dict[str, int]

    SIGN: Dict[str, str]
    ZERO: Set[str]
    DECIMAL_SEP: str
    DECIMAL_SYM: str

    AND_NUMS: Set[str]
    AND: str
    NEVER_IF_ALONE: Set[str]

    # Relaxed composed numbers (two-words only)
    # start => (next, target)
    RELAXED: Dict[str, Tuple[str, str]]

    simplify_check_coef_appliable: bool = False

    def native2chinese(self, word: str) -> Optional[str]:
        """Convert native number to chinese.
        Return None if word is not an native or is better left in letters.
        """
        return NotImplemented

    def ord2card(self, word: str) -> Optional[str]:
        """Convert ordinal number to cardinal.
        Return None if word is not an ordinal or is better left in letters.
        """
        return NotImplemented

    def num_ord(self, digits: str, original_word: str) -> str:
        """Add suffix to number in digits to make an ordinal"""
        return NotImplemented

    def normalize(self, word: str) -> str:
        return NotImplemented

    def not_numeric_word(self, word: Optional[str]) -> bool:
        return word is None or word != self.DECIMAL_SEP and word not in self.NUMBERS

    def split_number_word(self, word: str) -> str:  # maybe use: List[str]
        """In some languages numbers are written as one word, e.g. German
        'zweihunderteinundfünfzig' (251) and we might need to split the parts"""
        return NotImplemented