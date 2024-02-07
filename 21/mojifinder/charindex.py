import sys
from collections.abc import Iterator

import unicodedata
from collections import defaultdict

STOP_CODE = sys.maxunicode + 1
Char = str
Index = defaultdict[str, set[Char]]


def tokenize(text: str) -> Iterator[str]:
    for word in text.upper().replace('-', ' ').split():
        yield word


class InvertedIndex:
    entries: Index

    def __init__(self, start: int = 32, stop: int = STOP_CODE):
        entries: Index = defaultdict(set)
        for char in (chr(i) for i in range(start, stop)):
            name = unicodedata.name(char, '')
            if name:
                for word in tokenize(name):
                    entries[word].add(char)
        self.entries = entries

    def search(self, query: str) -> set[Char]:
        if words := list(tokenize(query)):
            found = self.entries[words[0]]
            return found.intersection(*(self.entries[w] for w in words[1:]))
        else:
            return set()


if __name__ == '__main__':
    # idx = InvertedIndex(32, 128)
    idx = InvertedIndex(32, )
    # print(idx.entries['DOLLAR'])
    # print(sorted(idx.entries['SIGN']))
    # print(idx.entries['A'] & idx.entries['SMALL'])
    # print(idx.search('capital a'))
    print(idx.search('car'))
