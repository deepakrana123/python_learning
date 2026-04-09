# convert x a integer to bit 

# check is even or odd
#  x%2==0 even otherwise odd , bitwise operator are much faster then the modular and add ,multiple,division and subtraction
# least significant bit is 1 or 0
#  x && 1=0 even and if 1 its equals to odd , its order of o(1)

# power of two x&&(x-1) if it euqls to zero then power of 2



# and or not xor operator in 
# 1&1=1,otherwise zero
# 1||1 or if one is true and other is false it gives true and if both true then also gives true , if both are false then its false
# xor is opposite of or it means not of or 
# not is opposite of everything



# print(bin(10))

# convert an interger to its binary
# n=19
# r=""
# while(n>0):
#     r=n%2
#     s=s+r
#     n=n//10
# print(r,"r")

# xor property is if two number are same it will give you zero
# set bit means number of position having 1
# right and left shift
# left shift means multiplication by 2 and right shift means divided by 2
# 12=1100
# left shift by 1=11000=24 , left shift means multiply by 2
# right shift by 1=110, right shift means divided by 2
# how to set ith bit
# if to check zeroth bit is set or not then i will take its and with 1
# how to detect if ith bit is set bit or nt
# 1<<k , k is the ith bit 
# how to set the ith bit of a number
# n||1<<k
# check the number of set bits
# m=123
# count=0
# while(m>0):
#     r=m%2
#     if r==1:
#         count+=1
#     n=n//10
# b=1101
# count=0
# while(b>0):
#     a=b and 1
#     if a==1:
#         count+=1
#     a=a>>1


# xor quriers of an array
# total sum of xor problems an xor sum problem


print("hi")


