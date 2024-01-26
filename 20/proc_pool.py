import sys
from concurrent import futures
from time import perf_counter
from typing import NamedTuple

from primes import is_prime, NUMBERS


class PrimeResult(NamedTuple):
    n: int
    flag: bool
    elapsed: float


def check(n: int):
    t0 = perf_counter()
    result = is_prime(n)
    elapsed = perf_counter() - t0
    return PrimeResult(n, result, elapsed)


def main():
    if len(sys.argv) < 2:
        workers = None
    else:
        workers = int(sys.argv[1])

    executor = futures.ProcessPoolExecutor(workers)
    actual_workers = executor._max_workers  # type: ignore

    print(f'Checking {len(NUMBERS)} numbers with {actual_workers} processes:')

    t0 = perf_counter()
    numbers = sorted(NUMBERS, reverse=True)
    with executor:
        for n, prime, elapsed in executor.map(check, numbers):
            label = 'P' if prime else ' '
            print(f'{n:16} {label} {elapsed:9.6f}s')

    time = perf_counter() - t0
    print(f'total time: {time:.2f}s')


if __name__ == '__main__':
    main()