from sympy import randprime

def generate_p():
    lower_bound = 2 ** 160
    upper_bound = 2 ** 161
    return randprime(lower_bound, upper_bound)

def read_message():
    open_read = open("initial_text.txt", "r")
    message =  open_read.read()
    open_read.close()
    return message

def string_to_bitstring(text):
    return ''.join(format(ord(c), '08b') for c in text)

def get_coeficients(given_power, m_text):
    power = given_power - 1
    number = 0
    m = list()
    for bit in string_to_bitstring(m_text):
        number += int(bit) * (2 ** power)
        power -= 1
        if power == -1:
            power = 159
            m.append(number)
            number = 0
    return m


def main():

    ### Encodare ###

    p = generate_p()
    print("P este: ", p)
    m_text = read_message()
    m_text_bit_len = len(m_text.encode('utf-8'))*8
    if m_text_bit_len/p.bit_length() == m_text_bit_len//p.bit_length():
        k = m_text_bit_len//p.bit_length()+1
    else:
        k = m_text_bit_len // p.bit_length() + 2

    m = get_coeficients(160, m_text)
    print("Coeficientii lui m:")
    print(m)

    print("~~Encoder~~")
    print("m este de lungime:", len(m))
    print("k este:", k)

    # testing
    # m = [2,3,4]
    # k = 5
    # p = 11

    s = 1   # numarul de greseli
    n = k + 2 * s   # lungimea encodarii
    print("Lungimea encodarii: ", n)

    # y_not_horner = list()  # encodarea simpla
    # for i in range(1, n+1):
    #     p_i = 0
    #     power = k - 2
    #     for coeff in m:
    #         p_i += coeff * pow(i,power,p)
    #         p_i = p_i % p
    #         power -= 1
    #     y_not_horner.append(p_i)
    # print(y_not_horner)

    y_horner = list()
    for i in range(1, n + 1):
        p_i = 0
        for coeff in m:  # Process coefficients in reverse order
            p_i = (p_i * i + coeff) % p
        p_i = (p_i * i) % p
        y_horner.append(p_i)
    print("y este: ")
    print(y_horner)

    open_write = open("encoding.txt", "w")
    open_write.write(str(y_horner))
    open_write.close()

    open_write = open("p.txt", "w")
    open_write.write(str(p))
    open_write.close()

if __name__=="__main__":
    main()