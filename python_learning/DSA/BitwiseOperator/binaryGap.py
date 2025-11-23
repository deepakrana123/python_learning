
def sumPrefixScores(words):
    a = []
    for word in words:
        b=[]
        for i in range(1, len(word) + 1):
            b.append(word[:i])
        a.append(b)
    abc=[]
    for word in a:
        count=0
        for w in word:
            for i in words:
                if i.startswith(w): 
                    count += 1
        abc.append(count)
    return abc

def rangeBitwiseAnd(left,right):
    if left==right:
        return left
    count=left
    for i in range(left+1,right+1):
        count&=i
    a=bin(left)
    c=bin(right)
    d=bin(4)
    print(a,c,d)
    print(count)
# print(rangeBitwiseAnd(left = 1, right = 2147483647))
def longestNiceSubarray(nums):
    currBit=0
    left=0
    right=0
    ans=-1
    while right<len(nums):
        while currBit&nums[right]!=0:
            currBit=currBit^nums[left]
            left+=1
        currBit=currBit|nums[right]
        ans=max(ans,right-left+1)
        right+=1
    return ans
# print(longestNiceSubarray([1,3,8,48,10]))
# def subarrayBitwiseORs(arr):
#     a=[]
#     for i in range(len(arr)):
#         for j in range(i,len(arr)):
#             a.append(arr[i:j+1])
#     dicts=[]
#     for i in range(len(a)):
#         c=0
#         for j in range(len(a[i])):
#             c|=a[i][j]
#         dicts.append(c)
#     d=set(dicts)
#     return len(d)

# print(subarrayBitwiseORs([1]))
def maximumTotalSum(maximumHeight):
    maximumHeight.sort(reverse=True)
    currHeight=maximumHeight[0]
    curr_Sum=0
    for height in maximumHeight:
        if currHeight>height:
            currHeight=height
        if currHeight<=0:
            return -1
        
        curr_Sum+=currHeight
        currHeight-=1
    print(maximumHeight,curr_Sum)
    
print(maximumTotalSum([2,2,1]))
def binaryGap(n):
        a=bin(n)[2:]
        ans=0
        prev=0
        print(a)
        for i in range(len(a)):
            if a[i]=='1':
                ans=max(ans,i-prev)
                prev=i
        return ans
print(binaryGap(22))
