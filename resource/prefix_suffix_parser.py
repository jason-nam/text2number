from typing import List


from typing import List

with open("prefix.txt", "r", encoding = 'utf-8') as file:
    prefixes = list()
    for line in file.readlines():
        try:
            prefixes.append(line.strip())
        except:
            pass

regex = "/^"
combined = "("