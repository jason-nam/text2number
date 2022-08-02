"""
Convert spelled numbers into numeric values or digit strings.
"""

from typing import List, Optional

from lang import Language

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
        self.int_builder = WordStreamValueParser(lang, relaxed=relaxed)
        self.frac_builder = WordStreamValueParser(lang, relaxed=relaxed)
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
        return True