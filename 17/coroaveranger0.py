from collections.abc import Generator


# def averager() -> Generator[float, float, None]:
def averager():
    total = 0.0
    count = 0
    average = 0.0
    while True:
        term = yield average
        total += term
        count += 1
        average = total / count
