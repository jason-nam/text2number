from typing import Dict, Optional, Set, Tuple

try:
    from .base import Language
except:
    from base import Language

MULTIPLIERS = {
    "십": 10,
    "백": 100,
    "천": 1000,
    "만": 10000,
    "억": 100000000,
    "조": 1000000000000,
    "경": 10000000000000000,
    "해": 100000000000000000000,
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

NATIVE_NUMBERS = NATIVE_MULTIPLIERS.copy()
NATIVE_NUMBERS.update(NATIVE_UNITS)
NATIVE_NUMBERS.update(NATIVE_MTENS)

class Korean(Language):

    MULTIPLIERS = MULTIPLIERS
    UNITS = UNITS
    NUMBERS = NUMBERS

    ZERO = {
        "영": "0",
        "공": "0",
    }

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