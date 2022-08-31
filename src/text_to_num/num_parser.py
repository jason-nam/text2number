"""
Convert spelled numbers into numeric values or digit strings.
"""

from typing import List, Optional

from .lang import Language, LANG

class WordStreamValueParserInterface:
    """Interface for language-dependent 'WordStreamValueParser'"""

    def __init__(self, lang: Language, relaxed: bool = False) -> None:
        """Initialize the parser."""
        self.lang = lang
        self.relaxed = relaxed

    def push(self, word: str, look_ahead: Optional[str] = None) -> bool:
        """Push next word from the stream."""
        return NotImplemented

    def parse(self, text: str) -> bool:
        """Parse whole text (or fail)."""
        return NotImplemented

    @property
    def value(self) -> int:
        """At any moment, get the value of the currently recognized number."""
        return NotImplemented


class WordStreamValueParserAsian(WordStreamValueParserInterface):
    """The actual value builder engine.
    The engine incrementaly recognize a stream of words as a valid number and build the
    corresponding numeric (integer) value.
    The algorithm is based on the observation that humans gather the
    digits by group of three to more easily speak them out.
    And indeed, the language uses powers of 10000 to structure big numbers.
    Public API:
        - ``self.push(word)``
        - ``self.value: int``
    """

    def __init__(self, lang: Language, relaxed: bool = False) -> None:
        """Initialize the parser.
        If ``relaxed`` is True, we treat the sequences described in
        ``lang.RELAXED`` as single numbers.
        """
        super().__init__(lang, relaxed)
        self.skip: Optional[str] = None
        self.n000_val: int = 0  # the number value part > 1000 or 10000
        self.grp_val: int = 0  # the current three/four digit group value
        self.last_word: Optional[
            str
        ] = None  # the last valid word for the current group

    @property
    def value(self) -> int:
        """At any moment, get the value of the currently recognized number."""
        return self.n000_val + self.grp_val

    def group_expects(self, word: str, update: bool = True) -> bool:
        """Does the current group expect ``word`` to complete it as a valid number?
        ``word`` should not be a multiplier; multiplier should be handled first.
        """
        expected = False
        if self.last_word is None:
            expected = True
        elif (
            self.last_word in self.lang.UNITS
            # and self.grp_val < 10
            or self.last_word in self.lang.STENS
            and self.grp_val < 20
        ):
            expected = (
                (
                    word in self.lang.UNITS
                    and self.relaxed
                ) or (
                    word in self.lang.THOUSAND
                    and self.grp_val < 1000
                ) or (
                    word in self.lang.HUNDRED
                    and self.grp_val % 1000 < 100
                ) or (
                    word in self.lang.TEN
                    and self.grp_val % 100 < 10
                )
            )
        elif self.last_word in self.lang.THOUSAND:
            expected = (
                word not in self.lang.THOUSAND
                and word not in self.lang.MTHOUSANDS
            )
        elif self.last_word in self.lang.HUNDRED:
            expected = (
                word not in self.lang.THOUSAND
                and word not in self.lang.MTHOUSANDS
                and word not in self.lang.HUNDRED
                and word not in self.lang.MHUNDREDS
            )
        elif self.last_word in self.lang.TEN:
            expected = (
                word not in self.lang.THOUSAND
                and word not in self.lang.MTHOUSANDS
                and word not in self.lang.HUNDRED
                and word not in self.lang.MHUNDREDS
                and word not in self.lang.TEN
                and word not in self.lang.MTENS
            )
        elif self.last_word in self.lang.MTHOUSANDS:
            expected = (
                word not in self.lang.MTHOUSANDS
                and word not in self.lang.THOUSAND
            )
        elif self.last_word in self.lang.MHUNDREDS:
            expected = (
                word not in self.lang.MTHOUSANDS
                and word not in self.lang.THOUSAND
                and word not in self.lang.MHUNDREDS
                and word not in self.lang.HUNDRED
            )
        elif self.last_word in self.lang.MTENS:
            expected = (
                word in self.lang.UNITS
                or word in self.lang.STENS
                and self.last_word in self.lang.MTENS_WSTENS
            )

        if update:
            self.last_word = word
        return expected

    def is_coef_appliable(self, coef: int) -> bool:
        if self.lang.simplify_check_coef_appliable:
            return coef != self.value

        """Is this multiplier expected?"""
        if self.value == 0:
            # number can start with a multiplier and multiplier can also
            # be declared when attached unit is 1 but the unit is not declared.
            # "일억" without unit would be "억".
            return True
        if coef > self.value and (self.value > 0 or coef == 10000):
            # a multiplier can be applied to anything lesser than itself,
            # as long as it not zero (special case for 10000 which then implies 1)
            return True
        if coef < self.n000_val:
            # a multiplier can not be applied to a value bigger than itself,
            # so it must be applied to the current group only.
            return (
                self.grp_val >= 0 or coef == 10000
            )  # "mille" without unit      is additive
        return False

    def push(self, word: str, look_ahead: Optional[str] = None) -> bool:
        """Push next word from the stream.
        Don't push punctuation marks or symbols, only words. It is the responsability
        of the caller to handle punctuation or any marker of pause in the word stream.
        The best practice is to call ``self.close()`` on such markers and start again after.
        Return ``True`` if  ``word`` contributes to the current value else ``False``.
        The first time (after instanciating ``self``) this function returns True marks
        the beginning of a number.
        If this function returns False, and the last call returned True, that means you
        reached the end of a number. You can get its value from ``self.value``.
        Then, to parse a new number, you need to instanciate a new engine and start
        again from the last word you tried (the one that has just been rejected).
        """
        if not word:
            return False

        if word == self.lang.AND and look_ahead in self.lang.AND_NUMS:
            return True

        word = self.lang.normalize(word)
        if word not in self.lang.NUMBERS:
            return False

        RELAXED = self.lang.RELAXED

        if word in self.lang.MULTIPLIERS:
            coef = self.lang.MULTIPLIERS[word]
            if not self.is_coef_appliable(coef):
                return False
            # a multiplier can not be applied to a value bigger than itself,
            # so it must be applied to the current group
            
            if coef < self.n000_val:
                self.n000_val = self.n000_val + coef * (
                    self.grp_val or 1
                )
            else:
                self.n000_val = (self.value or 1) * coef
            self.grp_val = 0
            self.last_word = None
        elif (
            self.relaxed
            and word in RELAXED
            and look_ahead
            and look_ahead.startswith(RELAXED[word][0])
            and self.group_expects(RELAXED[word][1], update=False)
        ):
            self.skip = RELAXED[word][0]
            self.grp_val += self.lang.NUMBERS[RELAXED[word][1]]
        elif self.skip and word.startswith(self.skip):
            self.skip = None
        elif self.group_expects(word):
            if word in self.lang.THOUSAND:
                self.grp_val = (
                    1000 * self.grp_val if self.grp_val else self.lang.THOUSAND[word]
                )
            elif word in self.lang.MTHOUSANDS:
                self.grp_val = self.lang.MTHOUSANDS[word]
            elif word in self.lang.HUNDRED:
                self.grp_val = (
                    100 * (self.grp_val % 10) + 10 * (self.grp_val // 10) if self.grp_val and (self.grp_val % 10) != 0 else self.grp_val + self.lang.HUNDRED[word]
                )
            elif word in self.lang.MHUNDREDS:
                self.grp_val = (
                    self.grp_val + self.lang.MHUNDREDS[word] if self.grp_val else self.lang.MHUNDREDS[word]
                )
            elif word in self.lang.TEN:
                self.grp_val = (
                    10 * (self.grp_val % 10) + 10 * (self.grp_val // 10) if self.grp_val and (self.grp_val % 10) != 0 else self.grp_val + self.lang.TEN[word]
                )
            elif word in self.lang.MTENS:
                self.grp_val = (
                    self.grp_val + self.lang.MTENS[word] if self.grp_val else self.lang.MTENS[word]
                )
            elif self.last_word in self.lang.UNITS and word in self.lang.UNITS and self.relaxed:
                self.grp_val = self.grp_val*10 + self.lang.NUMBERS[word]
            else:
                self.grp_val += self.lang.NUMBERS[word]
        else:
            self.skip = None
            return False
        return True


if __name__ == "__main__":
    texts = [
        []
    ]
    
    for t in texts:
        language: Language
        language = LANG["kr"]
        num_parser = WordStreamValueParserAsian(language, relaxed=False)
        
        for c in t:
            print(" ")
            print(c)
            num_parser.push(c)
        print(num_parser.value)