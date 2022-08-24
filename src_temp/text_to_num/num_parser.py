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
            else:
                self.grp_val += self.lang.NUMBERS[word]
        else:
            self.skip = None
            return False
        return True


class WordToDigitParser:
    """Words to digit transcriber.
    The engine incrementaly recognize a stream of words as a valid cardinal, ordinal,
    decimal or formal number (including leading zeros) and build the corresponding digit
    string.
    The submitted stream must be logically bounded: it is a phrase, it has a beginning
    and an end and does not contain sub-phrases. Formally, it does not contain punctuation
    nor voice pauses.
    For example, this text:
        « You don't understand. I want two cups of coffee, three cups of tea and an apple pie. »
    contains three phrases:
        - « you don't understand »
        - « I want two cups of coffee »
        - « three cups of tea and an apple pie »
    In other words, a stream must not cross (nor include) punctuation marks or voice pauses.
    Otherwise you may get unexpected, illogical, results. If you need to parse complete texts
    with punctuation, consider using `alpha2digit` transformer.
    Zeros are not treated as isolates but are considered as starting a new formal number
    and are concatenated to the following digit.
    Public API:
     - ``self.push(word, look_ahead)``
     - ``self.close()``
     - ``self.value``: str
    """

    def __init__(
        self,
        lang: Language,
        relaxed: bool = False,
        signed: bool = True,
        ordinal_threshold: int = 3,
    ) -> None:
        """Initialize the parser.
        If ``relaxed`` is True, we treat the sequence "quatre vingt" as
        a single "quatre-vingt".
        If ``signed`` is True, we parse signed numbers like
        « plus deux » (+2), or « moins vingt » (-20).
        Ordinals up to `ordinal_threshold` are not converted.
        """
        self.lang = lang
        self._value: List[str] = []
        self.int_builder = WordStreamValueParserAsian(lang, relaxed=relaxed)
        self.frac_builder = WordStreamValueParserAsian(lang, relaxed=relaxed)
        self.signed = signed
        self.in_frac = False
        self.closed = False  # For deferred stop
        self.open = False  # For efficiency
        self.last_word: Optional[str] = None  # For context
        self.ordinal_threshold = ordinal_threshold

    @property
    def value(self) -> str:
        """Return the current value."""
        return "".join(self._value)

    def close(self) -> None:
        """Signal end of input if input stream ends while still in a number.
        It's safe to call it multiple times.
        """
        if not self.closed:
            if self.in_frac and self.frac_builder.value:
                self._value.append(str(self.frac_builder.value))
            elif not self.in_frac and self.int_builder.value:
                self._value.append(str(self.int_builder.value))
            self.closed = True

    def at_start_of_seq(self) -> bool:
        """Return true if we are waiting for the start of the integer
        part or the start of the fraction part."""
        return (
            self.in_frac
            and self.frac_builder.value == 0
            or not self.in_frac
            and self.int_builder.value == 0
        )

    def at_start(self) -> bool:
        """Return True if nothing valid parsed yet."""
        return not self.open

    def _push(self, word: str, look_ahead: Optional[str]) -> bool:
        builder = self.frac_builder if self.in_frac else self.int_builder
        return builder.push(word, look_ahead)

    def is_alone(self, word: str, next_word: Optional[str]) -> bool:
        """Check if the word is 'alone' meaning its part of 'Language.NEVER_IF_ALONE'
        exceptions and has no other numbers around itself."""
        return (
            not self.open
            and word in self.lang.NEVER_IF_ALONE
            and self.lang.not_numeric_word(next_word)
            and self.lang.not_numeric_word(self.last_word)
            and not (next_word is None and self.last_word is None)
        )

    def push(self, word: str, look_ahead: Optional[str] = None) -> bool:
        """Push next word from the stream.
        Return ``True`` if  ``word`` contributes to the current value else ``False``.
        The first time (after instanciating ``self``) this function returns True marks
        the beginning of a number.
        If this function returns False, and the last call returned True, that means you
        reached the end of a number. You can get its value from ``self.value``.
        Then, to parse a new number, you need to instanciate a new engine and start
        again from the last word you tried (the one that has just been rejected).
        """
        if self.closed or self.is_alone(word, look_ahead):
            self.last_word = word
            return False

        if (
            self.signed
            and word in self.lang.SIGN
            and look_ahead in self.lang.NUMBERS
            and self.at_start()
        ):
            self._value.append(self.lang.SIGN[word])
        elif (
            word in self.lang.ZERO
            and self.at_start_of_seq()
            and (
                look_ahead is None
                or look_ahead in self.lang.NUMBERS
                or look_ahead in self.lang.ZERO
                or look_ahead in self.lang.DECIMAL_SEP
            )
        ):
            self._value.append("0")
        elif (
            word in self.lang.ZERO
            and self.at_start_of_seq()
            and look_ahead is not None
            and look_ahead in self.lang.DECIMAL_SEP
        ):
            pass
        elif self._push(self.lang.ord2card(word) or "", look_ahead):
            self._value.append(
                self.lang.num_ord(
                    str(
                        self.frac_builder.value
                        if self.in_frac
                        else self.int_builder.value
                    ),
                    word,
                )
                if self.int_builder.value > self.ordinal_threshold
                else word
            )
            self.closed = True
        elif (
            (word == self.lang.DECIMAL_SEP or word in self.lang.DECIMAL_SEP.split(','))
            and (look_ahead in self.lang.NUMBERS or look_ahead in self.lang.ZERO)
            and not self.in_frac
        ):
            if not self.value:
                self._value.append(str(self.int_builder.value))
            self._value.append(self.lang.DECIMAL_SYM)
            self.in_frac = True
        elif not self._push(word, look_ahead):
            if self.open:
                self.close()
            self.last_word = word
            return False

        self.open = True
        self.last_word = word
        return 


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