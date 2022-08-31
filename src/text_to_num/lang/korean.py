from typing import Dict, Optional, Set, Tuple

try:
    from .language import Language
except:
    from language import Language

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

STENS: Dict[str, int] = {}

TEN: Dict[str, int] = {"십": 10}

MTENS: Dict[str, int] = {
    word: value * 10
    for value, word in enumerate(
        "이십 삼십 사십 오십 육십 칠십 팔십 구십".split(), 2
    )
}

MTENS_WSTENS: Set[str] = set()

HUNDRED = {"백": 100}

MHUNDREDS: Dict[str, int] = {
    word: value * 100
    for value, word in enumerate(
        "이백 삼백 사백 오백 육백 칠백 팔백 구백".split(), 2
    )
}

THOUSAND = {"천": 1000}

MTHOUSANDS: Dict[str, int] = {
    word: value * 1000
    for value, word in enumerate(
        "이천 삼천 사천 오천 육천 칠천 팔천 구천".split(), 2
    )
}

CTENS: Dict[str, int] = {
    "".join((ten_word, unit_word)): ten_val + unit_val
    for ten_word, ten_val in MTENS.items()
    for unit_word, unit_val in UNITS.items()
}

CHUNDREDS: Dict[str, int] = {
    "".join((hundred_word, cten_word)): hundred_val + cten_val
    for hundred_word, hundred_val in MHUNDREDS.items()
    for cten_word, cten_val in CTENS.items()
}

CHUNDREDS.update({
    "".join((hundred_word, unit_word)): hundred_val + unit_val
    for hundred_word, hundred_val in MHUNDREDS.items()
    for unit_word, unit_val in UNITS.items()
})

CHUNDREDS.update({
    "".join((hundred_word, ten_word)): hundred_val + ten_val
    for hundred_word, hundred_val in MHUNDREDS.items()
    for ten_word, ten_val in MTENS.items()
})

CTHOUSANDS: Dict[str, int] = {
    "".join((thousand_word, cten_word)): thousand_val + cten_val
    for thousand_word, thousand_val in MTHOUSANDS.items()
    for cten_word, cten_val in CTENS.items()
}

CTHOUSANDS.update({
    "".join((thousand_word, chundred_word)): thousand_val + chundred_val
    for thousand_word, thousand_val in MTHOUSANDS.items()
    for chundred_word, chundred_val in CHUNDREDS.items()
})

CTHOUSANDS.update({
    "".join((thousand_word, unit_word)): thousand_val + unit_val
    for thousand_word, thousand_val in MTHOUSANDS.items()
    for unit_word, unit_val in UNITS.items()
})

CTHOUSANDS.update({
    "".join((thousand_word, ten_word)): thousand_val + ten_val
    for thousand_word, thousand_val in MTHOUSANDS.items()
    for ten_word, ten_val in MTENS.items()
})

CTHOUSANDS.update({
    "".join((thousand_word, hundred_word)): thousand_val + hundred_val
    for thousand_word, thousand_val in MTHOUSANDS.items()
    for hundred_word, hundred_val in MHUNDREDS.items()
})

COMPOSITES = CTENS.copy()
COMPOSITES.update(CHUNDREDS)
COMPOSITES.update(CTHOUSANDS)

NUMBERS = MULTIPLIERS.copy()
NUMBERS.update(UNITS)
NUMBERS.update(TEN)
NUMBERS.update(MTENS)
NUMBERS.update(HUNDRED)
NUMBERS.update(MHUNDREDS)
NUMBERS.update(THOUSAND)
NUMBERS.update(MTHOUSANDS)
# NUMBERS.update(COMPOSITES)

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

NATIVE_NUMBERS = NATIVE_MULTIPLIERS.copy()
NATIVE_NUMBERS.update(NATIVE_UNITS)
NATIVE_NUMBERS.update(NATIVE_MTENS)

class Korean(Language):

    MULTIPLIERS = MULTIPLIERS
    UNITS = UNITS
    STENS = STENS
    TEN = TEN
    MTENS = MTENS
    MTENS_WSTENS = MTENS_WSTENS
    HUNDRED = HUNDRED
    MHUNDREDS = MHUNDREDS
    THOUSAND = THOUSAND
    MTHOUSANDS = MTHOUSANDS
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
        Return None if word is not a native number.
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