from typing import List


from typing import List
import json

with open("resource/prefix.txt", "r", encoding = 'utf-8') as file:
    prefixes = list()
    for line in file.readlines():
        try:
            prefixes.append(line.strip())
        except:
            pass

with open("prefix.json", "w", encoding="utf-8") as file:
    json.dump(prefixes, file, ensure_ascii=False)

regex = "/^"
combined = "("