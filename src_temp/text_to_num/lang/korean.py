from typing import Dict, Optional, Set, Tuple

try:
    from .base import Language
except:
    from base import Language

MULTIPLIERS = {
    "만": 1_0000,
    "억": 1_0000_0000,
    "조": 1_0000_0000_0000,
    "경": 1_0000_0000_0000_0000,
    "해": 1_0000_0000_0000_0000_0000,
}

UNITS: Dict[str, int] = {
    "일": 1,
    "이": 2,
    "삼": 3,
    "사": 4,
    "오": 5,
    "육": 6,
    "칠": 7,
    "팔": 8,
    "구": 9,
}

STENS: Dict[str, int] = {"십": 10}

HUNDRED = {"백": 100}

THOUSAND = {"천": 1000}

NATIVE_MULTIPLIERS = {
    "열": "십",
    "온": "백",
    "즈믄": "천",
    "골": "만",
    "잘": "억",
    "울": "조",
}

NATIVE_UNITS = {
    "하나": "일",
    "둘": "이",
    "셋": "삼",
    "넷": "사",
    "다섯": "오",
    "여섯": "육",
    "일곱": "칠",
    "여덟": "팔",
    "아홉": "구",
}

NATIVE_MTENS = {
    "스물": "이십",
    "서른": "삼십",
    "마흔": "사십",
    "쉰": "오십",
    "예순": "육십",
    "일흔": "칠십",
    "여든": "팔십",
    "아흔": "구십",
}

NUMBERS = MULTIPLIERS.copy()
NUMBERS.update(UNITS)
NUMBERS.update(STENS)
NUMBERS.update(HUNDRED)
NUMBERS.update(THOUSAND)


NATIVE_NUMBERS = NATIVE_MULTIPLIERS.copy()
NATIVE_NUMBERS.update(NATIVE_UNITS)
NATIVE_NUMBERS.update(NATIVE_MTENS)

class Korean(Language):

    MULTIPLIERS = MULTIPLIERS
    UNITS = UNITS
    STENS = STENS
    HUNDRED = HUNDRED
    THOUSAND = THOUSAND
    NUMBERS = NUMBERS

    SIGN = {"더하기": "+", "빼기": "-"}
    ZERO = {"영", "공",}
    DECIMAL_SEP = "점"
    DECIMAL_SYM = "."

    AND_NUMS: Set[str] = set()
    AND = " "
    NEVER_IF_ALONE = {}

    RELAXED: Dict[str, Tuple[str, str]] = {}

    simplify_check_coef_appliable: bool = False

    def native2chinese(self, word: str) -> Optional[str]:
        """Convert native number to chinese.
        Return None if word is not an ordinal or is better left in letters.
        """

        suff = True if any(num in word for num in NATIVE_NUMBERS) else False
        if not (suff):
            return None
        else:
            source = word
            for nums in NATIVE_NUMBERS:
                if nums in source:
                    source = source.replace(nums, NATIVE_NUMBERS[nums])
        return source

    def ord2card(self, word: str) -> Optional[str]:
        """Convert ordinal number to cardinal.
        Return None if word is not an ordinal or is better left in letters.
        """

        suff = word.startswith("제")
        if not (suff):
            return None
        else:
            source = word[1:]
        if source not in self.NUMBERS:
            return None
        return source

    def num_ord(self, digits: str, original_word: str) -> str:
        """Add suffix to number in digits to make an ordinal"""
        
        sf = original_word[:1] if original_word.startswith("제") else ""
        return f"{sf}{digits}"

    def normalize(self, word: str) -> str:
        return word

# self = ""
# print(Korean.native2chinese(self, "마흔둘"))