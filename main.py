from ciphers import *
import timeit

cipher= PolybiusSquare()
msg = "Hello worlds!12341 5342 dslflds zxczxc.--3213                    .1!" * 50

#encrypt = cipher.encrypt(msg)
#print(encrypt)
#print(cipher.decrypt(encrypt))

time1 = timeit.timeit(lambda: cipher.encrypt(msg), number=10000)
time2 = timeit.timeit(lambda: cipher.encrypt1(msg), number=10000)
print(time1)
print(time2)