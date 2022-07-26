BAD_WORDS = [
    "삼삼오오",
]


def remove_bad_words(numbers: list) -> list:
    for bad_word in BAD_WORDS:
        numbers = list(filter(lambda a: a != bad_word, numbers))
    return numbers