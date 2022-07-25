def TextIntoList(text_name: str) -> list:
    """text안에 있는 것들을 리스트로 변환해준다"""

    file_number = open(text_name,'r',encoding="UTF-8")
    in_list = file_number.readlines()
    for i, line in enumerate(in_list):
        in_list[i] = line.strip()
    file_number.close()
    return in_list

def TextIntoPair(text_name: str)-> list:
    """text안에 line 2개별로 한개의 묶음으로"""

    file_number = open(text_name,'r',encoding="UTF-8")
    in_list = file_number.readlines()
    for i, line in enumerate(in_list):
        in_list[i] = line.strip()
    file_number.close()
    pair_list = []
    for i in range(0,len(in_list),2):
        pair_list.append((in_list[i],in_list[i+1]))
    return pair_list

if __name__ == "__main__":
    None