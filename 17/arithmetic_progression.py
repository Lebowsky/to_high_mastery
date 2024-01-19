class ArithmeticProgression:
    def __init__(self, begin, step, end=None):
        self.begin = begin
        self.step = step
        self.end = end

    def __iter__(self):
        result_type = type(self.begin + self.step)

        result = result_type(self.begin)
        forever = self.end is None
        index = 0

        while forever or result < self.end:
            yield result
            index += 1
            result = self.begin + self.step * index


def aritprog_gen(begin, step, end=None):
    result = type(begin + step)(begin)
    forever = end is None
    index = 0
    while forever or result < end:
        yield result
        index += 1
        result = begin + step * index


if __name__ == '__main__':
    # ap = ArithmeticProgression(0, 1, 3)
    ap = aritprog_gen(0, 1, 3)
    print(list(ap))

    # ap = ArithmeticProgression(1, .5, 3)
    ap = aritprog_gen(1, .5, 3)
    print(list(ap))

    from fractions import Fraction

    # ap = ArithmeticProgression(0, Fraction(1, 3), 1)
    ap = aritprog_gen(0, Fraction(1, 3), 1)
    print(list(ap))

    from decimal import Decimal

    # ap = ArithmeticProgression(0, Decimal('.1'), .3)
    ap = aritprog_gen(0, Decimal('.1'), .3)
    print(list(ap))
