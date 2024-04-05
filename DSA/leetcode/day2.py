def maxDepth(s):
    if len(s)==0:
        return 0
    b=[]
    result=0
    for key in s:
        if key =="(":
            b.append(key)
        elif key == ")":
            b.pop()
        result=max(len(b),result)
    return result
            
print(maxDepth("(1)+((2))+(((3)))"))

# def isSorted(arr,n):
#     for i in range(1,n):
#         if arr[i-1]>arr[i]:
#             return False
#     return True
# # t=int(input())
# for _ in range(t):
#     n,k=map(int,input().split())
#     arr=list(map(int,input().split()))
#     if isSorted(arr,len(arr)):
#         print("true")
#     elif k>=2:
#         print("true")
#     else:
#         print("No")
def makeGood(s):
    t=[]
    for i in range(len(s)):
        if len(t)>0 and s[i].isupper() and t[-1]==s[i].lower():
            t.pop()
        elif t and s[i].islower() and t[-1]==s[i].upper():
            t.pop()
        else:
            t.append(s[i])
    return "".join(t)
print(makeGood("Pp"))
print(makeGood( "leEeetcode"))

        
    
    
        