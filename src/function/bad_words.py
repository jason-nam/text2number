from util import loader

path = "../data/dict/bad_words.txt"

BAD_WORDS = loader.load_list(path)


def remove_bad_words(numbers: list) -> list:
    for bad_word in BAD_WORDS:
        numbers = list(filter(lambda a: a != bad_word, numbers))
    return numbers