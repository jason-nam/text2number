import re
from itertools import dropwhile
from typing import Any, Iterator, List, Sequence, Tuple, Union, Optional

try:
    from .lang import LANG, Language
    from .parsers import (
        WordStreamValueParserInterface,
        WordStreamValueParser, 
        WordToDigitParser,
    )
except:
    from lang import LANG, Language
    from parsers import (
        WordStreamValueParserInterface,
        WordStreamValueParser, 
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
    num_parser = WordStreamValueParser(language, relaxed=relaxed)
    tokens = list(dropwhile(lambda x: x in language.ZERO, text.split()))
    tokens = list(dropwhile(lambda x: x in language.ZERO, text))
    print(tokens)
    if not all(
        num_parser.push(word, ahead) 
        for word, ahead in look_ahead(tokens)
    ):
        raise ValueError("invalid literal for text2num: {}".format(repr(text)))

    return num_parser.value


def alpha2digit(
    text: str,
    lang: str,
    relaxed: bool = False,
    signed: bool = True,
    ordinal_threshold: int = 3,
) -> str:
    """Return the text of ``text`` with all the ``lang`` spelled numbers converted to digits.
    Takes care of punctuation.
    Set ``relaxed`` to True if you want to accept some disjoint numbers as compounds.
    Set ``signed`` to False if you don't want to produce signed numbers, that is, for example,
    if you prefer to get « minus 2 » instead of « -2 ».
    Ordinals up to `ordinal_threshold` are not converted.
    """
    if lang not in LANG:
        raise Exception("Language not supported")

    language = LANG[lang]
    segments = re.split(
        r"\s*[\.,;\(\)…\[\]:!\?]+\s*", text
    )
    punct = re.findall(r"\s*[\.,;\(\)…\[\]:!\?]+\s*", text)
    if len(punct) < len(segments):
        punct.append("")

    # Default
    out_segments: List[str] = []
    for segment, sep in zip(segments, punct):
        tokens = segment.split()
        num_builder = WordToDigitParser(
            language,
            relaxed=relaxed,
            signed=signed,
            ordinal_threshold=ordinal_threshold,
        )
        in_number = False
        out_tokens: List[str] = []
        for word, ahead in look_ahead(tokens):
            if num_builder.push(word.lower(), ahead and ahead.lower()):
                in_number = True
            elif in_number:
                out_tokens.append(num_builder.value)
                num_builder = WordToDigitParser(
                    language,
                    relaxed=relaxed,
                    signed=signed,
                    ordinal_threshold=ordinal_threshold,
                )
                in_number = num_builder.push(word.lower(), ahead and ahead.lower())
            if not in_number:
                out_tokens.append(word)
        # End of segment
        num_builder.close()
        if num_builder.value:
            out_tokens.append(num_builder.value)
        out_segments.append(" ".join(out_tokens))
        out_segments.append(sep)
    text = "".join(out_segments)
    return text


if __name__ == "__main__":
    print(text2num("구조이천오백이십삼억오백만칠천사백육십일", "kr"))
    print(text2num("오천이백", "kr"))
    
    # print(text2num("삼삼오오", "kr"))

    count = "104080043691234"
    nstring = ["", "십", "백", "천", "만", "십", "백", "천", "억", "십", "백", "천", "조", "십", "백", "천"]
    nlist = list(count)
    nlen = len(count)
    nd = {
        "1": "일",
        "2": "이",
        "3": "삼",
        "4": "사",
        "5": "오",
        "6": "육",
        "7": "칠",
        "8": "팔",
        "9": "구",
        "0": ""
    }
    nlen = nlen - 1
    for i in nlist:
        if i == "0":
            nlen -= 1
            continue
        else:
            print(f"{nd[i]}{nstring[nlen]}", end="")
            nlen -= 1
