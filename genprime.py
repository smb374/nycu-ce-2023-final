from montgomery import Montgomery, Residue, transform, randodd
from small_prime import SMALL_PRIMES
from random import randrange


class PrimeTestContext:
    n: int
    mont: Montgomery
    one: Residue
    two: Residue
    n1: Residue

    def __init__(self, n: int, bits: int) -> None:
        self.n = n
        self.mont = Montgomery(n, bits)
        self.one = transform(1, self.mont)
        self.two = transform(2, self.mont)
        self.n1 = transform(n - 1, self.mont)

    def baille_psw(self) -> bool:
        if self.n == 0:
            return False
        elif (self.n & 1) == 0:
            return False
        # Trial division
        for p in SMALL_PRIMES:
            if self.n == p:
                return True
            elif self.n % p == 0:
                return False
        return self.fermat() and self.miller_rabin()

    def fermat(self) -> bool:
        return self.two.exp_mod(self.n - 1) == self.one

    def miller_rabin(self) -> bool:
        r = 0
        d = self.n - 1
        while (d & 1) == 0:
            d >>= 1
            r += 1
        for _ in range(10):
            cont = False
            a = randrange(2, self.n - 2)
            ar = Residue(a, self.mont)
            x = ar.exp_mod(d)
            if x == self.one or x == self.n1:
                continue
            for _ in range(r - 1):
                x = x * x
                if x == self.n1:
                    cont = True
                    break
            if cont:
                continue
            return False
        return True


def get_prime(bits: int) -> int:
    while True:
        p = randodd(bits)
        ctx = PrimeTestContext(p, bits)
        if ctx.baille_psw():
            return p


if __name__ == "__main__":
    p = get_prime(512)
    print(f"Found a prime = {p}.")
