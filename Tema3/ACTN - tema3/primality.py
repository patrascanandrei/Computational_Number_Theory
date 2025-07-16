import math
import random
import time

def is_prime(n):
    if n<=1: return 0
    if n == 2: return 1
    if n%2 == 0 : return 0
    root = int(math.sqrt(n))
    for i in range(3, root + 2, 2):
        if n % i == 0: return 0
    return 1

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

def modularization(a, n):
    # bin_a = bin(a)[2:]
    # difference = 2*n - len(bin_a)
    # bin_a = '0'*difference + bin_a
    # # while len(bin_a) < 2*n:
    # #     bin_a = '0' + bin_a
    # a0 = 0
    # a1 = 0
    # index = 0
    # for i in range(2*n-1, n-1, -1):
    #     if bin_a[i] == '1':
    #         a0 += pow(2, index)
    #     index +=1
    # index = 0
    # for i in range(n-1, -1, -1):
    #     if bin_a[i] == '1':
    #         a1 += pow(2, index)
    #     index +=1
    # number = pow(2, n)-1
    # if a1+a0 < number:
    #     return a1+a0
    # elif a1+a0 == 2*number:
    #     return 0
    # else:
    #     return a1+a0-number

    mask = (1 << n) - 1
    a0 = a & mask
    a1 = (a >> n) & mask
    total = a0 + a1
    if total < mask:
        return total
    elif total == 2 * mask:
        return 0
    else:
        return total - mask

class Numbers:
    def __init__(self, given_number):
        self.number = given_number

    def solovay_strassen(self):
        if self.number%2 == 0:
            return False
        a = random.randrange(2, self.number-1)
        jacobi = jacobi_symbol(a, self.number)
        if jacobi== 0:
           return False
        else:
           if legendre_symbol(a, self.number) != jacobi:
               return False
           else:
               return True  # probabil prim

    def lucas_lehmer_good_modularization(self):
        n = len(bin(self.number))-2
        if is_prime(n) == 0:
            return False
        u = 4
        k = 0
        while k<n-2:
            # u = (u*u-2)%self.number
            u = modularization( (u*u-2) , n )
            k += 1
        if u!=0: return False
        return True

    def lucas_lehmer_slow_modularization(self):
        n = len(bin(self.number))-2
        if is_prime(n) == 0:
            return False
        u = 4
        k = 0
        while k<n-2:
            # u = (u*u-2)%self.number
            # u = modularization( (u*u-2) , n )
            u = (u*u-2) % (2 ** n - 1)
            k += 1
        if u!=0: return False
        return True

print("-------------Solovay-Strassen----------------")
x = Numbers(170141183460469231731687303715884105727)
counter = 200
false_hit = 0
while counter:
    result = x.solovay_strassen()
    # print(result)
    counter -=1
    if not result:
        print(f"{x.number} nu este prim")
        false_hit = 1
        break
if false_hit == 0: print(f"{x.number} este aproape sigur prim")

x = Numbers(170141183460469231731687303715884105729)
counter = 200
while counter:
    result = x.solovay_strassen()
    # print(result)
    counter -=1
    if not result:
        print(f"{x.number} nu este prim")
        false_hit = 1
        break
if false_hit == 0: print(f"{x.number} este aproape sigur prim")

print("-------------Lucas-Lehmer----------------")

y = Numbers(7) # n = 3, prim, la curs

start_time = time.time()
print(f"Este {y.number} prim: ", y.lucas_lehmer_good_modularization())
end_time = time.time()
elapsed_time = end_time - start_time
print("Timp modularizare rapida: ", elapsed_time)

start_time = time.time()
print(f"Este {y.number} prim: ", y.lucas_lehmer_slow_modularization())
end_time = time.time()
elapsed_time = end_time - start_time
print("Timp modularizare %: ", elapsed_time)

y = Numbers(31) # n=5, prim

start_time = time.time()
print(f"Este {y.number} prim: ", y.lucas_lehmer_good_modularization())
end_time = time.time()
elapsed_time = end_time - start_time
print("Timp modularizare rapida: ", elapsed_time)

start_time = time.time()
print(f"Este {y.number} prim: ", y.lucas_lehmer_slow_modularization())
end_time = time.time()
elapsed_time = end_time - start_time
print("Timp modularizare %: ", elapsed_time)

y = Numbers(170141183460469231731687303715884105727)

start_time = time.time()
print(f"Este {y.number} prim: ", y.lucas_lehmer_good_modularization())
end_time = time.time()
elapsed_time = end_time - start_time
print("Timp modularizare rapida: ", elapsed_time)

start_time = time.time()
print(f"Este {y.number} prim: ", y.lucas_lehmer_slow_modularization())
end_time = time.time()
elapsed_time = end_time - start_time
print("Timp modularizare %: ", elapsed_time)

y = Numbers(6864797660130609714981900799081393217269435300143305409394463459185543183397656052122559640661454554977296311391480858037121987999716643812574028291115057151) # n=6, nu e prim

start_time = time.time()
print(f"Este {y.number} prim: ", y.lucas_lehmer_good_modularization())
end_time = time.time()
elapsed_time = end_time - start_time
print("Timp modularizare rapida: ", elapsed_time)

start_time = time.time()
print(f"Este {y.number} prim: ", y.lucas_lehmer_slow_modularization())
end_time = time.time()
elapsed_time = end_time - start_time
print("Timp modularizare %: ", elapsed_time)

print("-------------Modularizare Mersenne----------------")
print(modularization(15, 2))
# numarul de modularizat e 15, nr Mersenne e 2^2-1 = 3 -> 15%3 = 0

print(modularization(15, 3))
# numarul de modularizat e 15, nr Mersenne e 2^3-1 = 7 -> 15%7 = 1
