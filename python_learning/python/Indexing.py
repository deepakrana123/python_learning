import numpy as np


a=np.arange(10)**4

print(a)
print(a[2])
a[0:4:2]=100
print(a)
a[:6:2]=100
print(a)