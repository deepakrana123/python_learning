a=[2,1,4,3]
for i in range(0,len(a)):
    for j in range(i,len(a)):
        for k in range(j,len(a)):
            if a[i]<a[j]>a[k]:
                # print(a[i],a[j],a[k])
                break
# def iters(a):
#     if len(a)<3:
#         return 0
#     i=0
#     trip=[]
#     min_Element=float("inf")
#     max_Element=float("-inf")
#     for i in range(len(a)):
#         if a[i]<max_Element:
#             trip.append([min_Element,max_Element,a[i]])
#         else:
#             min_Element = min(min_Element,a[i])
#             max_Element = max(max_Element,a[i])
#     return trip
# print(iters(a))

def fillbucket(s):
    count=0
    cnt=0
    isThree=False
    for ch in s:
        if ch=='.':
            cnt+=1
            count+=1
        else:
            cnt=0
        if cnt==3:
            isThree=True
            break
    if isThree:
        return 2
    else:
        return count
            
# print(fillbucket('....'))
def minOperations(nums, k):
    result=0
    for num in nums:
        result=result^num
    result=bin(result^k).replace("0b", "")
    count=0
    for i in range(len(result)):
        if result[i]=='1':
            count+=1
    return count
# print(minOperations([2,1,3,4],1))

def compress(s):
    c=0
    for i in range(len(s)):
        if s[i]!='0':
            return s[i:]
    return 0
def compareVersion(version1, version2):
    a=version1.split('.')
    b=version2.split('.')
    if len(a)>len(b):
        c=len(a)-len(b)
        while c>0:
            b.append('0')
            c-=1
    elif len(a)<len(b):
        c=len(b)-len(a)
        while c>0:
            a.append('0')
            c-=1
    for i in range(len(a)):
        a[i]=compress(a[i])
        b[i]=compress(b[i])
    for i in range(len(a)):
        if int(a[i]) > int(b[i]):
            return 1
        elif int(a[i])<int(b[i]):
            return -1
    return 0
# print(compareVersion("1.01","1.001"))
def reversePrefix(word, ch):
    chIndex=0
    for i in range(len(word)):
        if word[i]== ch:
            chIndex=i
            break
    a=word[0:chIndex+1]
    b=word[chIndex+1:]
    return a[::-1]+b
        
print(reversePrefix("abcdefd","d"))
        
     
    