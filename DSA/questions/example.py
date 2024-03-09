def linearSearch(arr,num):
    for i in range(len(arr)):
        if num==arr[i]:
            return i
    raise IndexError("No index found")

# def union(arr1,arr2):
#     d={}
#     e=[]
#     f= set()
#     for num in arr1:
#         if d.get(num) is not None:
#             d[num]+=1
#         else:
#             d[num]=1
#     for num in arr2:
#         if d.get(num) is not None:
#             d[num]+=1
#         else:
#             d[num]=1
#     for n in d:
#         e.append(n)
#     for num in arr1:
#         f.add(num)
#     for num in arr2:
#         f.add(num)
#     ws=[]
#     n=len(arr1)
#     m=len(arr2)
#     i=0
#     j=0
#     while i<n and j<m:
#         if arr1[i]<=arr2[j]:
#             if len(ws)==0 or ws[-1]!=arr1[i]:
#                 ws.append(arr1[i])
#             i+=1
#         else:
#             if len(ws)==0 or ws[-1]!=arr2[j]:
#                 ws.append(arr1[j])
#             j+=1
#     while i < m: 
#         if ws[-1] != arr1[i]:
#             ws.append(arr1[i])
#         i+=1
#     while j < n: 
#         if ws[-1] != arr1[i]:
#             ws.append(arr1[i])
#         j+=1
#     return ws

#     # return f

def twiceElementInArr(arr):
    elem=0
    for i in range(len(arr)):
        elem = elem^arr[i]
    return elem
# print(union({1,2,3,4,5},{2,3,4,4,5}))
# print(twiceElementInArr([4, 1, 2, 1, 2/]),"a")
def findMaxConsecutiveOnes(nums):
    max1=float("-inf")
    val=0
    for i in range(len(nums)):
        if(nums[i]==1):
            val+=1
        elif nums[i]!=1:
            val=0
        max1=max(max1,val)
    return max1
# print(findMaxConsecutiveOnes([1,0,1,1,0,1]))

def minimumLength(s):
    m=0
    n=len(s)-1
    while(m<n and s[m]==s[n]):
        ch=s[m]
        while(m<n and ch==s[m]):
            m+=1
        while(n>m and ch==s[n]):
            n-=1
       
        
    return n-m+1

# def largestNumber(nums):
    
#     print(nums)

# largestNumber([3,30,34,5,9])
# def printLogestCommonSubsequence(s1,s2):
#     t=dp=[[0 for j in range(len(s1)+1)] for i in range(len(s2))]
def markCol(matrix,m,n,j):
    for i in range(n):
        if matrix[i][j]!=0:
            matrix[i][j]=-1
def markRow(matrix,m,n,i):
    for j in range(m):
        if matrix[i][j]!=0:
            matrix[i][j]=-1

def setZeros(a):
    m=len(a)
    n=len(a[0])
    for i in range(m):
        for j in range(n):
            if(a[i][j]==0):
                markRow(a,m,n,i)
                markCol(a,m,n,j)
    for i in range(m):
        for j in range(n):
            if a[i][j]==-1:
                a[i][j]=0
    return a
# print(setZeros([[1, 1, 1], [1, 0, 1], [1, 1, 1]]))

def rotateMatrix(a):
    m=len(a)
    n=len(a[0])
    dp=[[0 for j in range(n)] for i in range(m)]
    for i in range(m):
        for j in range(n):
            dp[i][j]=a[n-j-1][m-i-1]
    dp.reverse()
    # print(dp)
rotateMatrix([[1,2,3],[4,5,6],[7,8,9]])
def rearrange(a):
    even=[]
    odd=[]
    for num in a:
        if num<0:
            odd.append(num)
        else:
            even.append(num)
    for i in range(len(a)//2):
        a[2*i]=even[i]
        a[2*i+1]=odd[i]
    return a
def rearrange1(a):
    pos=0
    neg=1
    ans=[0]*(len(a))
    for i in range(len(a)):
        # print(i,"i")
        if a[i]<0:
            ans[neg]=a[i]
            neg+=2
        elif pos<len(a):
            ans[pos]=a[i]
            pos+=2
    return ans
# print(rearrange1([1,2,-4,-5]))


def lonestSubarray(a,k):
    n=len(a)
    max1=float("-inf")
    for i in range(len(a)):
        sum1=a[i]
        for j in range(i+1,len(a)):
            sum1+=a[j]
            if(sum1==k):
                max1=max(max1,j-i+1)
    return max1
# print(lonestSubarray([2, 3, 5, 1, 9],10))
def isIsomorphic(s,t):
    dict1={}
    if len(s)!=len(t):
        return False
    for i in range(len(s)):
        if(dict1.get(s[i])):
            if dict1[s[i]]!=t[i]:
                return False
        else:
            dict1[s[i]]=t[i]
    return True
# print(isIsomorphic("egg","ade"))
def reverseWords(s):
    spaceIndex=0
    a=[]
    for i in range(len(s)):
        if s[i]==' ':
            a.append(s[spaceIndex:i])
            spaceIndex=i+1
    a.append(s[spaceIndex:len(s)])
    return a[::-1]
print(reverseWords("the sky is blue"))
def frequencySort(s):
        dict1={}
        for i in range(len(s)):
            if dict1.get(s[i]):
                dict1[s[i]]+=1
            else:
                dict1[s[i]]=1
        a=dict(sorted(dict1.items(), key=lambda item: item[1], reverse=True))
        strs=""
        for keys in a:
            strs+=keys
        print(strs.strip())
print(frequencySort("tree"))
    
    
        

            
            
                