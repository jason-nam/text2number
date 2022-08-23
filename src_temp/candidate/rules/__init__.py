import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from candidate.rules.sentence_parser import BringNumber, PutNumber
from candidate.rules.tag_correction import correct_tags
