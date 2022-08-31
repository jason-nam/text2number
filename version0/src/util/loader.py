def load_dictionary(path):
    result = {}
    with open(path, 'r', encoding="utf8") as file:
        for line in file.readlines():
            try:
                key = line.split("\t")[0]
                value = line.split("\t")[1]
                result[key] = str(value).strip()
            except Exception as e:
                pass
    return result

def load_list(path):
    result = []
    with open(path, 'r', encoding="utf8") as file:
        for line in file.readlines():
            try:
                result.append(line.strip())
            except:
                pass
    return result

if __name__ == "__main__":
    None