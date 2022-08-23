import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from candidate.exception.bad_words import remove_bad_words
from candidate.exception.month_exception import get_month_exception
from candidate.exception.lang_dict import  apply_dictionary, revert_error_words
from candidate.exception.pattern_language import convert_regular_expression, revert_regular_expression, convert_text_regular_expression
from candidate.exception.phone_number import ApplyPhoneNumberDigit