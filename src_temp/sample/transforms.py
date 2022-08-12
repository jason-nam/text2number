import re
from itertools import dropwhile
from typing import Any, Iterator, List, Sequence, Tuple, Union, Optional

import sys
sys.path.append(__file__)

from lang import LANG, Language, Korean
from parsers import WordToDigitParser

USE_PT_ORDINALS_MERGER = True

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

    # Process segments
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
        out_tokens: List[str] = []
        # End of segment
        num_builder.close()
        if num_builder.value:
            out_tokens.append(num_builder.value)
        out_segments.append(" ".join(out_tokens))
        out_segments.append(sep)
    text = "".join(out_segments)

    return text

if __name__ == "__main__":
    print(alpha2digit("십일", "kr"))
    None