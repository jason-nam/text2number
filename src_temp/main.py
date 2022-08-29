from .candidate import candidate_extract
from .text_to_num import text2num
from .exception import (
    apply_dictionary, 
    revert_error_words,
    get_month_exception,
    convert_regular_expression,
    revert_regular_expression,
    convert_text_regular_expression,
    ApplyPhoneNumberDigit
)

def main(sent: str) -> None:
    return