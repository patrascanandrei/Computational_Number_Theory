import ast
import random
from sympy import randprime

open_read = open("encoding.txt", "r")
encoding =  open_read.read()
encoding = ast.literal_eval(encoding)

# print(encoding[1])      # works
# print(len(encoding))    # 23

random_index = random.randint(0,len(encoding)-1)
lower_bound = 2 ** 160
upper_bound = 2 ** 161
change =  randprime(lower_bound, upper_bound)
encoding[random_index] = abs(encoding[random_index] - change)

open_write = open("corrupt_encoding.txt", "w")
open_write.write(str(encoding))

open_read.close()
open_write.close()
