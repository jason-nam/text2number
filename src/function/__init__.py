import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from function.bad_words import remove_bad_words
from function.convert import get_number, digit2txt
from function.month_exception import get_month_exception
from function.new_language import  apply_dictionary, revert_error_words
from function.pattern_language import apply_regular_expression
from function.phone_number import phone_number_exception
from function.sentence_parser import BringNumber, PutNumber
from function.tag_correction import subject_case_marker, apply_tag_correction, fixing_Baek_Bum, fixing_Han_Il, fixing_BaekJe, fixing_NR_after_MM, fixing_NR_after_NNB, fixing_per_person
