from typing import Self
import random


class Montgomery:
    N: int
    N_NEG_INV: int
    R: int
    R2: int
    R_MASK: int
    BITS: int

    def __init__(self, modulus: int, bits: int):
        self.N = modulus
        self.BITS = bits
        self.R = 1 << self.BITS
        self.R2 = (1 << (self.BITS << 1)) % self.N
        self.R_MASK = self.R - 1
        self.N_NEG_INV = self.R - pow(self.N, -1, self.R)

    def __eq__(self, rhs: Self) -> bool:
        return self.N == rhs.N and self.R == rhs.R

    # T -> TR^-1 (mod N)
    def reduce(self, T: int) -> int:
        m = ((T & self.R_MASK) * self.N_NEG_INV) & self.R_MASK
        t = (T + m * self.N) >> self.BITS
        if t >= self.N:
            return t - self.N
        return t


class Residue:
    x: int
    mont: Montgomery

    def __init__(self, x: int, mont: Montgomery):
        self.x = x
        self.mont = mont

    def __str__(self) -> str:
        return f"Residue({self.x})"

    def __mul__(self, rhs: Self) -> Self:
        assert self.mont == rhs.mont
        new_x = self.mont.reduce(self.x * rhs.x)
        return Residue(new_x, self.mont)

    def __eq__(self, rhs: Self) -> bool:
        return self.x == rhs.x

    def exp_mod(self, exp: int) -> Self:
        prod = transform(1, self.mont)
        base = self
        while exp.bit_length() > 0:
            if (exp & 1) == 1:
                prod *= base
            exp >>= 1
            base *= base
        return prod

    def recover(self) -> int:
        return self.mont.reduce(self.x)


# x -> xR (mod N)
def transform(x: int, mont: Montgomery) -> Residue:
    return Residue(x * mont.R % mont.N, mont)


# x -> x^(-1) * R' (mod N), R' = 2^k, R = 2^n, n <= k <= 2n
def almost_inverse(a: int, mont: Montgomery) -> tuple[int, int]:
    assert 1 <= a <= mont.N
    u = mont.N
    v = a
    r = 0
    s = 1
    k = 0
    while v > 0:
        if (u & 1) == 0:
            u >>= 1
            s <<= 1
        elif (v & 1) == 0:
            v >>= 1
            r <<= 1
        elif u > v:
            u = (u - v) >> 1
            r += s
            s <<= 1
        else:
            v = (v - u) >> 1
            s += r
            r <<= 1
        k += 1
    if r >= mont.N:
        r -= mont.N
    return (mont.N - r, k)


def randint(bits: int) -> int:
    data = random.randbytes(bits // 8)
    return int.from_bytes(data, "little")


def randodd(bits: int) -> int:
    while True:
        x = randint(bits)
        if (x & 1) == 1:
            return x


if __name__ == "__main__":
    bits = 1024
    m = 750791094644726559640638407699
    x1 = 540019781128412936473322405310
    x2 = 515692107665463680305819378593

    mont = Montgomery(m, bits)
    x1m = transform(x1, mont)
    assert x1m.exp_mod(x2).recover() == pow(x1, x2, m)
