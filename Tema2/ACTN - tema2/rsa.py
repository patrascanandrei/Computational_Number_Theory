import copy
import math
from sympy import randprime, mod_inverse
import time

def left_to_right_binary_method(x, n, m) -> (int, int):
    bin_array = bin(n)
    k = len(bin_array)
    y = 1
    count1s = 0
    for i in range(2, k):
        y = (y*y) %m
        if bin_array[i]=='1':
            y=(y*x) % m
            count1s+=1
    return y, int(math.log2(n))+count1s-1

def left_to_right_b_ary_method(x, n, m, beta):
    n_copy = copy.deepcopy(n)
    x_array = [0] * beta
    x_array[0] = 1
    for i in range(1, beta):
        x_array[i] = (x_array[i-1]*x)%m
    representation = []
    while n>0:
        representation.insert(0, n % beta)
        n = n//beta
    y = 1
    for i in range(0, len(representation)):
        y = pow(y, beta) % m
        y = (y * x_array[representation[i]]) %m

    return y, int(math.log(n_copy, 2)) + len(representation)

def left_to_right_sliding_window(x, n, m, w):
    x_powers = [0] * pow(2,w)
    x_powers[1], x_powers[2] = x % m, (x*x) % m
    for omega in range(3, pow(2,w),2):
        x_powers[omega] = (x_powers[omega-2]*x_powers[2]) % m
    bin_array_n = bin(n)[2:]
    k = len(bin_array_n)
    y = 1
    i = 0
    while i<k:
        if bin_array_n[i] == '0':
            y = (y*y) %m   # ridicari la puterea 2
            i += 1
        else:
            l = min(w, k-i)
            while l>1 and bin_array_n[i+l-1] == '0':
                l-=1
            exponent = int(bin_array_n[i:i+l], 2)

            for _ in range(l): y = (y*y) %m  # ridicari la puterea 2

            y = (y * x_powers[exponent]) % m
            i+=l
    return y, int(math.log2(n))+ int(k/(w+1))

def garner(v_array, m_array):
    t = len(v_array) - 1
    c_array = [0] * (t+1)
    for i in range(2, t+1):
        c_array[i] = 1
        for j in range(1, i):
            u = pow( m_array[j], (m_array[i]-2), m_array[i]) % m_array[i]
            u = mod_inverse(m_array[j], m_array[i])
            c_array[i] = (u*c_array[i]) % m_array[i]
    u = v_array[1]
    x = u
    m_prod = m_array[1]
    for i in range(2, t+1):
        u = ((v_array[i] - x)*c_array[i]) % m_array[i]
        x = x + u * m_prod
        m_prod *= m_array[i]
    return x

def generate_large_number(bits):
    lower_bound = 2 ** (bits-1)
    upper_bound = 2 ** bits
    return randprime(lower_bound, upper_bound)

def main():
    print("----Multiprime RSA----")
    p,q,r = 0,0,0
    while p==q or p==r or q==r:
        p = generate_large_number(700)
        q = generate_large_number(700)
        r = generate_large_number(700)
    print("p: ",p)
    print("q: ",q)
    print("r: ",r)
    n = p*q*r
    e = pow(2,16)+1     # nr prim, va fi coprim cu phi(n)
    phi_n = (p-1)*(q-1)*(r-1)
    d = mod_inverse(e, phi_n)      # invers modular al e in raport cu phi(n)

    # d = pow(e, (phi_n-2), phi_n) # gresit, phi nu este prim

    # mesajul initial
    x = 232462344526523146457243514
    print("Mesajul in clar: ", x)
    y = pow(x, e, n)
    print("Mesajul encriptat: ", y)

    start_time = time.time()
    x_decr_power1 = pow(y, d, n)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print("Mesajul decriptat cu ridicare clasica la putere: ", x_decr_power1)
    print("Timp: ", elapsed_time)

    start_time = time.time()
    # garner
    b_vector = [0,0,0,0]
    # ------------------------------Lanturi aditive -----------------------------------------

    # b_vector[1] = pow((y % p), d % (p-1), p)
    binary= left_to_right_binary_method( (y%p), d % (p-1), p)
    b_vector[1] = binary[0]
    print("Lungime lant aditiv(met. binara): ", binary[1])

    # b_vector[2] = pow((y % q), d % (q-1), q)
    b_ary = left_to_right_b_ary_method((y%q), d % (q-1), q, 8)
    b_vector[2] = b_ary[0]
    print("Lungime lant aditiv(fereastra fixa): ", b_ary[1])

    # b_vector[3] = pow((y % r), d % (r-1), r)

    sliding = left_to_right_sliding_window((y % r), d % (r-1), r, 5)
    b_vector[3] = sliding[0]
    print("Lungime lant aditiv(fereastra mobila): ", sliding[1])

    x_decr_multiprime = garner(b_vector, [0,p,q,r])
    end_time = time.time()
    elapsed_time = end_time - start_time
    print("Mesajul decriptat cu TCR(Garner): ", x_decr_multiprime)
    print("Timp: ", elapsed_time)

    print("----Multipower RSA----")
    p, q = 0, 0
    while p == q:
        p = generate_large_number(700)
        q = generate_large_number(700)
    print("p: ", p)
    print("q: ", q)
    n = p * p * q
    e = pow(2, 16) + 1  # nr prim, va fi coprim cu phi(n)
    phi_n = (p * p - p) * (q - 1)
    d = mod_inverse(e, phi_n)  # invers modular al e in raport cu phi(n)

    y = pow(x, e, n)
    print("Mesajul encriptat: ", y)

    start_time = time.time()
    x_decr_power2 = pow(y, d, n)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print("Mesajul decriptat cu ridicare clasica la putere: ", x_decr_power2)
    print("Timp: ", elapsed_time)

    start_time = time.time()
    # multipower, hansel
    b_vector = [0, 0, 0]
    b_vector[2] = pow((y % q), d % (q - 1), q)

    x_0 = pow((y % p), d % (p - 1), p)
    x_1 = ((y - pow(x_0, e, p*p)) //p * mod_inverse(e*pow(x_0, e-1, p*p),p)) % p
    b_vector[1] = x_1*p+x_0

    x_decr_multipower = garner(b_vector, [0, p*p, q])

    end_time = time.time()
    elapsed_time = end_time - start_time
    print("Mesajul decriptat cu TCR: ", x_decr_multipower)
    print("Timp: ", elapsed_time)

    print("----Lanturi aditive pentru multiprime RSA----")
    print(left_to_right_binary_method(3,13,100))
    print(left_to_right_b_ary_method(3,13,100, 8))
    print(left_to_right_sliding_window(3,13,100, 3))

if __name__=="__main__":
    main()