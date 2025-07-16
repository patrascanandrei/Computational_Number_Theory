import ast
import copy
import subprocess
from itertools import combinations
from math import comb
import time

def simultaneous_inversion(p, a):
    k = len(a)-1
    c = [0, a[1]]
    a_inverse = [0] * (k+1)
    for i in range(2, k+1):
        c.append( (c[i-1]*a[i])%p )
    u = pow(c[k], (p - 2), p) %p
    for i in range(k,1,-1):
        a_inverse[i] = (u*c[i-1]) %p
        u = (u * a[i]) % p
    a_inverse[1] = u
    return a_inverse

def two_pol_mul(a_coef, b_coef, p):
    a_len = len(a_coef)
    b_len = len(b_coef)
    result_coef = [0] * (a_len + b_len - 1)

    for i in range(a_len):
        for j in range(b_len):
            result_coef[i + j] += a_coef[i] * b_coef[j]
            result_coef[i + j] %= p

    return result_coef

def decoding_set(a_set, k_inverses_pos, k_inverses_neg, z, p):
    x_results = [0] * len(a_set)

    for i in a_set:
        a_set_no_element = a_set.copy()
        a_set_no_element.remove(i)
        a_coef = [1]

        for j in a_set_no_element:
            if (i - j) > 0:
                b_coef = [k_inverses_pos[i - j], (-k_inverses_pos[i - j] * j) % p]
            else:
                b_coef = [k_inverses_neg[j - i], (-k_inverses_neg[j - i] * j) % p]

            a_coef = two_pol_mul(a_coef, b_coef, p)

        for j in range(len(a_coef)):
            a_coef[j] = (a_coef[j] * z[i - 1]) % p

        for j in range(len(x_results)):
            x_results[j] = (x_results[j] + a_coef[j]) % p

    return x_results

def main():
    files = ["encoder.py", "noise_gen.py"]
    for file in files:
        subprocess.run(["python", file])

    print("~~Decoder~~")
    open_read = open("corrupt_encoding.txt", "r")
    z =  open_read.read()
    z = ast.literal_eval(z)
    open_read.close()
    print("z este: ")
    print(z)

    open_read = open("p.txt", "r")
    p = open_read.read()
    p = int(p)
    open_read.close()

    # -- Testing
    # print(encoding[1])      # works
    # print(len(encoding))    # 23
    # z = [11,0,6,5,8]
    # p = 11
    # print("P este: ", p)

    k = len(z) - 2     # scazut 2*s, s = 1
    i_set = {i for i in range(1,len(z)+1)}

    # metoda cu k*(k-1) inversari
    a_set = list(combinations(i_set, k))
    start_time = time.time()
    fc = 1
    iterations = 0
    a_set1 = []
    while fc !=0 and iterations < comb(len(z), k):
        a_set1 = list(a_set[iterations])
        # print(a_set1)
        fc = 0
        for i in a_set1:
            a_set_no_element = copy.deepcopy(a_set1)
            a_set_no_element.remove(i)
            result = 1
            for j in a_set_no_element:
                result *= ((j * pow( (j-i), (p-2), p))%p )
            fc += (z[i-1] * result)
        fc %= p
        # print("(k(k-1))Fc este: ",fc)
        iterations +=1
    end_time = time.time()
    print("(k(k-1))Subset A pentru care fc = 0: ", a_set1)
    elapsed_time = end_time - start_time
    print(f"Elapsed time: {elapsed_time:.6f} seconds")

    # metoda cu k* inversari
    start_time = time.time()
    fc = 1
    iterations = 0
    a_set2 = []
    k_inverses_pos = [0]
    for index in range(1, k+3):
        k_inverses_pos.append( pow(index, (p - 2), p))
    k_inverses_neg = [0]
    for index in range(1, k+3):
        k_inverses_neg.append( pow(p-index, (p - 2), p))

    # print("(k)Inversi pozitivi: ",k_inverses_pos)
    # print("(k)Inversi negativi: ", k_inverses_neg)

    while fc !=0 and iterations <comb(len(z), k):
        a_set2 = list(a_set[iterations])
        # print(a_set2)
        fc = 0
        for i in a_set2:
            a_set_no_element = copy.deepcopy(a_set2)
            a_set_no_element.remove(i)
            result = 1
            for j in a_set_no_element:
                if (j-i)>0:
                    result *= ( (j * k_inverses_pos[j-i])%p )
                else:
                    result *= ( (j * k_inverses_neg[-1*(j-i)])%p )
            fc += (z[i-1] * result)
        fc %= p
        # print("(k)Fc este: ",fc)
        iterations +=1
    end_time = time.time()
    print("(k)Subset A pentru care fc = 0: ", a_set2)
    elapsed_time = end_time - start_time
    print(f"Elapsed time: {elapsed_time:.6f} seconds")

    # metoda cu 1 inversare
    start_time = time.time()
    fc = 1
    iterations = 0
    a_set3 = []
    k_inverses_pos = simultaneous_inversion(p, [i for i in range(0,k+3)])
    k_inverses_neg = simultaneous_inversion(p, [p-i for i in range(0,k+3)])
    # print("(1)Inversi pozitivi: ",k_inverses_pos)
    # print("(1)Inversi negativi: ", k_inverses_neg)
    while fc != 0 and iterations < comb(len(z), k):
        a_set3 = list(a_set[iterations])
        # print(a_set3)
        fc = 0
        for i in a_set3:
            a_set_no_element = copy.deepcopy(a_set3)
            a_set_no_element.remove(i)
            result = 1
            for j in a_set_no_element:
                if (j-i)>0:
                    result *= ((j * k_inverses_pos[j - i]) % p)
                else:
                    result *= ((j * k_inverses_neg[i-j]) % p)
            fc += (z[i - 1] * result)
        fc %= p
        # print("(1)Fc este: ", fc)
        iterations += 1
    end_time = time.time()
    print("(1)Subset A pentru care fc = 0: ", a_set3)
    elapsed_time = end_time - start_time
    print(f"Elapsed time: {elapsed_time:.6f} seconds")

    print("Decoding:")
    print(decoding_set(a_set3, k_inverses_pos, k_inverses_neg, z, p))


if __name__ == "__main__":
    main()