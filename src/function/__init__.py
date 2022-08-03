import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from function.bad_words import remove_bad_words
from function.convert import txt_to_digit, digit_to_txt
from function.month_exception import get_month_exception
from function.new_language import  apply_dictionary, revert_error_words
from function.pattern_language import convert_regular_expression, revert_regular_expression, convert_text_regular_expression
from function.phone_number import phone_number_exception
from function.sentence_parser import BringNumber, PutNumber
from function.tag_correction import correct_tags
