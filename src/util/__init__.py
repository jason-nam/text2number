import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from util.loader import load_dictionary, load_list
from util.pos import get_pos, get_morphs
from util.transform_index import get_txt_ind, get_pos_ind 
