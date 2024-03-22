from dataclasses import dataclass
from typing import NamedTuple

from pympler import asizeof  # pip install pympler


@dataclass(frozen=True, slots=True)
class UserDataclass:
    pk: int
    name: str


class UserNamedTuple(NamedTuple):
    pk: int
    name: str


if __name__ == '__main__':
    print(asizeof.asizeof(UserDataclass(1, 'And')))  # 136
    print(asizeof.asizeof(UserNamedTuple(1, 'And')))  # 144
