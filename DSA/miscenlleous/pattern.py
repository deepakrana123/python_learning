# for i in range(1,5):
#     for j in range(1,5):
#         print(j,end="")
#         # end="" to end the row
#     print("\r")
# # print("\r") to end the line

count=1
# for i in range(0,3):
#     for j in range(0,3):
#         print(count , end="")
#         count=count+1
#     print("\r")

# for i in range(0,5):
#     value=i
#     for j in range(0,i):
#         # print(j)
#         print(value, end="")
#         value=value+1
#     print("\r")

# for i in range(0,4):
#     for j in range(0,i):
#         print("#" , end="")
#     print("\r")
               
# counts=1
# for i in range(0,4):
#     for j in range(0,i):
#         print(counts , end="")
#         counts=counts+1
#     print("\r")
               
# for i in range(4,0,-1):
#     for j in range(i,0,-1):
#         print(i , end="")
#         # counts=counts+1
#     print("\r")
for i in range(1,4):
    for j in range(1,i):
        # print(i,j)
        print(i+j-1 , end="")
        # counts=counts+1
    print("\r")
               
# print(chr(ord('A') + 1))
# for i in range(1,4):
#     for j in range(1,4):
#         print(chr(ord('A') + i-1),end="")
#         # counts=counts+1
#     print("\r")

# for i in range(1,4):
#     for j in range(1,4):
#         print(chr(ord('A') + j-1),end="")
#         # counts=counts+1
#     print("\r")
count=0
for i in range(1,4):
    for j in range(1,4):
        print(chr(ord('A') + count),end="")
        count=count+1
        # counts=counts+1
    print("\r")
               