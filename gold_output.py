
import os
import json
import re
from difflib import SequenceMatcher
import copy

import os
import sys
# sys.path.append("../../src")
# print(os.path.dirname(os.path.abspath(__file__)))
# sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# sys.path.append("../../src")
from src.main import main

def korean2num(sent: str) -> str:
    """worker function"""
    return main(sent)

regex_str = r'[0-9]+'
regex = re.compile(regex_str)

gold_path = "../data/gold/"
gold_file_path_list = list()

input_path = "../data/input/"
input_file_path_list = list()

test_path = "./gold_data/"
test_file_path_list = list()


def save_file_path(dir_path):
    file_path_list = list()
    for (root, directories, files) in os.walk(dir_path):
        for file in files:
            if '.json' in file:
                file_path_list.append(file) 
    return file_path_list

def otherStr(string1, string2):
    match = SequenceMatcher(None, string1, string2)
    string1_copy = copy.deepcopy(string1)
    string2_copy = copy.deepcopy(string2)
    for tag, i1, i2, j1, j2 in match.get_opcodes():
        if(tag == "equal"):
            if(string1[i1:i2] != " "):
                string1_copy = string1_copy.replace(string1[i1:i2], "@#")
            if(string2[j1:j2] != " "):
                string2_copy = string2_copy.replace(string2[j1:j2], "@#")
    return list(filter(None,[i.strip() for i in list(filter(None, string1_copy.split("@#")))])), list(filter(None,[j.strip() for j in list(filter(None, string2_copy.split("@#")))]))

def makeOutputData(input_data, gold_data):
    datas = list()
    for input_item in input_data["document"]["utterance"]:
        id = input_item["id"]
        speaker_id = input_item["speaker_id"]
        input_form = input_item["form"]
        temp= dict()
        temp["id"] = id
        temp["input"] = input_form
        for gold_item in gold_data["document"]["utterance"]:
            if(id == gold_item["id"]):
                temp["output"] = gold_item["form"]
                temp["isChange"] = 0
                temp["word"] = list()
                temp["digit"] = list()
                digit_str = regex.search(temp["output"])
                if(digit_str != None):
                    temp["isChange"] = 1
                    word, digit = otherStr(temp["input"], temp["output"])
                    temp["word"] = word
                    temp["digit"] = digit
                datas.append(temp)
    return datas
## 디렉토리 생성 함수
def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' +  directory)
        
def make_json_file(datas, file_path):
    with open(file_path, 'w', encoding="utf8") as make_file:
        json.dump(datas, make_file, ensure_ascii=False, indent="\t")
        
if __name__ == "__main__":
    input_file_path_list = save_file_path(input_path)
    gold_file_path_list = save_file_path(gold_path)

    test_file_path_list = save_file_path(test_path)
    for file_path in test_file_path_list:
        with open(os.path.join(test_path,file_path), 'r', encoding='utf8') as f_test:
            test_data = json.load(f_test)

        for ind, test_item in enumerate(test_data):
            new_isChange = 0
            string1 = test_item["input"]
            print(string1)
            new_output = korean2num(string1)
            print(new_output)
            new_word, new_digit = otherStr(string1, new_output)
            if new_digit != []:
                new_isChange = 1
            test_data[ind]["new_output"] = new_output
            test_data[ind]["new_isChange"] = new_isChange
            test_data[ind]["new_word"] = new_word
            test_data[ind]["new_digit"] = new_digit

        output_file_path = "./gold_data_out/"
        make_json_file(test_data, output_file_path+str(file_path))

    # for file_path in gold_file_path_list:
    #     try:
    #         with open(os.path.join(gold_path,file_path), 'r', encoding='utf8') as f_gold:
    #             gold_data = json.load( f_gold)
    #         if(file_path in input_file_path_list):
    #             with open(os.path.join(input_path,file_path), 'r', encoding='utf8') as f_input:
    #                 input_data = json.load(f_input)
    #         else:
    #             print("@@@@@@@@")
    #             print(file_path)
    #             continue
    #     except Exception as e:
    #         print(e)
    #         print(file_path)
    #         continue
    #     output_file_path = "../data/testset/"
    #     createFolder(output_file_path)
    #     datas = makeOutputData(input_data, gold_data)
    #     make_json_file(datas, output_file_path+str(file_path))
    #     print("complete!!", output_file_path+str(file_path) )
    
    
    
        