import random
from sympy import isprime, mod_inverse
import math

def generate_prime(bits):
    while True:
        number = random.randint(2**(bits-1), 2**bits-1)
        if isprime(number):
            return number


def prime_factors(n):
    factors = set()
    while n%2 == 0:
        factors.add(2)
        n //= 2
    for i in range(3, int(math.sqrt(n))+1, 2):
        while n % i == 0:
            factors.add(i)
            n //= i
    if n>2:
        factors.add(n)
    return factors


def primitive_root(p):
    phi = p-1
    factors = prime_factors(phi)
    while True:
        ok = 1
        local_alpha = random.randint(2, p - 2)
        for f in factors:
            if pow(local_alpha, phi // f, p) == 1:
                ok = 0
                break
        if ok:
            return local_alpha

def shanks(given_alpha, given_beta, given_p):
    m = math.sqrt(given_p-1)
    if m != int(m): m+=1
    m = int(m)

    # baby steps
    l_list = dict()
    for j in range(0, m):
        l_list[j] = pow(given_alpha, j, given_p)
    l_list = dict(sorted(l_list.items(), key=lambda item: item[1]))

    # giant steps
    alpha_to_minus_m = pow(given_alpha, m, given_p)
    alpha_to_minus_m = mod_inverse(alpha_to_minus_m, given_p)
    searched_i = -1
    searched_j = -1
    for i in range(0, m):
        to_compare = (given_beta*pow(alpha_to_minus_m, i, given_p))%given_p
        for item in l_list.items():
            if to_compare == item[1]:
                searched_i = i
                searched_j = item[0]
                break
        if searched_i !=-1: break
    return searched_i * m + searched_j


# print("-------Radacina primitiva-------")
# generated_p = generate_prime(32)
# print(f"Generated prime p: {generated_p}")
# alpha = primitive_root(generated_p)
# print(f"Primitive root for prime {generated_p} is: {alpha}")
#
# print("--------Logaritm discret--------")
# searched_power0 = shanks(2, 11, 13)
# print(f"Discrete logarithm for class example: {searched_power0}")
#
# beta = random.randint(0, generated_p - 1)
# searched_power1 = shanks(alpha, beta, generated_p)
# print(f"Discrete logarithm for beta {beta}: {searched_power1}")
#
# print(f"Verify", pow(alpha, searched_power1, generated_p), "=", beta)

print("------------------- Setup Silver-Pohlig-Hellman -------------------------")

def generate_1024bit_multiple():
    # e multiplu de 2, 3, si 5
    lcm = 30
    while True:
        num = random.getrandbits(1024)
        num -= num % lcm  # multiplu de 30
        if num.bit_length() == 1024:
            return num

def jacobi_symbol(a, m):
    a = a%m
    if a == 0 or a==1:
        return a
    if a == 2:
        return -1 if m%8 in (3,5) else 1

    if a%2 == 0:
        return jacobi_symbol(2, m) * jacobi_symbol(a//2, m)

    if a%4 == 3 and m%4 == 3:
        return -jacobi_symbol(m,a)
    else:
        return jacobi_symbol(m,a)

def legendre_symbol(a, n):
    euler = pow(a, (n-1)//2, n)
    if euler == n-1: return -1
    return euler

def solovay_strassen(x):
    if x%2 == 0:
        return False
    a = random.randrange(2, x-1)
    jacobi = jacobi_symbol(a, x)
    if jacobi== 0:
       return False
    else:
       if legendre_symbol(a, x) != jacobi:
           return False
       else:
           return True  # probabil prim

searched_p = -1
false_hit = 0
while searched_p == -1:
    x = generate_1024bit_multiple()
    counter = 30
    false_hit = 0
    while counter:
        result = solovay_strassen(x+1)
        counter -=1
        if not result:
            false_hit = 1
            break
    if false_hit == 0:
        searched_p = x+1

exponents = (searched_p-1) / 30
print(exponents)