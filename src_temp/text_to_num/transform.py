import re
from itertools import dropwhile
from typing import Any, Iterator, List, Sequence, Tuple, Union, Optional

from .lang import LANG, Language, Korean
from .num_parser import (
    WordStreamValueParserInterface,
    WordStreamValueParserAsian, 
    WordToDigitParser,
)

def look_ahead(sequence: Sequence[Any]) -> Iterator[Tuple[Any, Any]]:
    """Look-ahead iterator.
    Iterate over a sequence by returning couples (current element, next element).
    The last couple returned before StopIteration is raised, is (last element, None).
    Example:
    >>> for elt, nxt_elt in look_ahead(sequence):
    ... # do something
    """
    maxi = len(sequence) - 1
    for i, val in enumerate(sequence):
        ahead = sequence[i + 1] if i < maxi else None
        yield val, ahead


def text2num(
    text: str, 
    lang: Union[str, Language], 
    relaxed: bool = False
) -> int:
    """Convert the ``text`` string containing an integer number written as letters
    into an integer value.
    Set ``relaxed`` to True if you want to accept "quatre vingt(s)" as "quatre-vingt"
    (fr) or "ein und zwanzig" as "einundzwanzig" (de) etc..
    Raises an ValueError if ``text`` does not describe a valid number.
    Return an int.
    """
    language: Language
    # mypy seems unable to understand this
    language = LANG[lang] if type(lang) is str else lang  # type: ignore
    num_parser: WordStreamValueParserInterface

    # Default
    if type(language) is Korean:
        num_parser = WordStreamValueParserAsian(language, relaxed=relaxed)
        tokens = list(dropwhile(lambda x: x in language.ZERO, text))
    else:
        raise ValueError("invalid lang type for text2num: {}".format(repr(lang)))

    if not all(
        num_parser.push(word, ahead) 
        for word, ahead in look_ahead(tokens)
    ):
        raise ValueError("invalid literal for text2num: {}".format(repr(text)))

    return num_parser.value


if __name__ == "__main__":
    None