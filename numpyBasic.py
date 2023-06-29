import numpy as np
from numpy import pi
# numpy array have a single value and size are fixed 
# a = np.arange(20).reshape(4,5)
# # a=np.arange(10)
# # print(a)
# # print(a.shape , "shape")
# # print(a.ndim,"ndim")
# # print(a.dtype.name)


# # numpy array having zeros

# b=np.zeros((2,3,4) ,dtype=np.int16)

# # print(b)


# c=np.arange(2,6,0.5)
# print(c)


# print(np.linspace(0,2,9))

# x=np.linspace(0,pi*2,100)
# print(np.sin(x))



A = np.array([[1, 1],
              [0, 1]])
B = np.array([[2, 0],
              [3, 4]])

print(A+B)
print(A-B)
print(A*B)  
# linear multiplication element wise multiplication
print(A.dot(B))
# matrix multiplication