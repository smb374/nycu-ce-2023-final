from genprime import get_prime
from math import log

p = get_prime(1024)
q = get_prime(1024)
n = p * q
r = (p - 1) * (q - 1)
e = 65537
d = pow(e, -1, r)

print(f"N: {n:x}, bit size = {(int(log(n, 256)) + 1) * 8}")
print(f"e: {e:x}")
print(f"d: {d:x}")

pt = b"Hello World!"
ct = pow(int.from_bytes(pt, "big"), e, n)
pt2 = bytes.fromhex(f"{pow(ct, d, n):x}")
print(f"pt = {pt}, ct = {ct:x}, ct^d = {pt2}")
