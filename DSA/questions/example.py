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
    t=dp=[[0 for j in range(len(s1)+1)] for i in range(len(s2))]
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

def rotateMatrix(a):
    m=len(a)
    n=len(a[0])
    dp=[[0 for j in range(n)] for i in range(m)]
    for i in range(m):
        for j in range(n):
            dp[i][j]=a[n-j-1][m-i-1]
    dp.reverse()
    # print(dp)
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
def reverseWords(s):
    spaceIndex=0
    a=[]
    for i in range(len(s)):
        if s[i]==' ':
            a.append(s[spaceIndex:i])
            spaceIndex=i+1
    a.append(s[spaceIndex:len(s)])
    str1=""
    for i in range(len(a)-1,-1,-1):
        if a[i]=='':
            continue
        else:
            str1+=a[i] +' '
    return str1
def reverseWords1(s):
    p1=0
    p2=0
    d=[]
    while(p1<len(s) and p2<len(s)):
        if s[p1]==' ' and s[p1]!='':
            if p1>p2:
                d.append(s[p2:p1])
            p2=p1+1
        p1+=1
    if p2<p1:
        d.append(s[p2:p1])
    d.reverse()
    return " ".join(d)     
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
        return strs.strip()
def longestCommonPrefix(strs):
    ans=""
    for n in zip(*strs):
        if len(set(n))==1:
            ans+=n[0]
    return ans
def intersection(nums1, nums2):
        a=set()
        i=0
        j=0
        c=sorted(nums1)
        d=sorted(nums2)
        print(c,d)
        while(i<len(c) and j<len(d)):
            if(c[i]>d[j]):
                j+=1
            elif(c[i]<d[j]):
                i+=1
            else:
                a.add(c[i])
                i+=1
                j+=1
        
        return list(a)
def longestSubarray(arr,k):
    max1=float("-inf")
    for i in range(len(arr)):
        sum=0
        for j in range(i,len(arr)):
            sum+=arr[j]
            if sum==k:
                max1=max(max1,j-i+1)
    print(max1)
def twoSum(arr,target):
    for i in range(len(arr)):
        for j in range(i+1,len(arr)):
            if arr[i]+arr[j]==target:
                return [i,j]

def twoSum1(arr,target):
    dict1={}
    for i in range(len(arr)):
        a=target-arr[i]
        if arr[i] in dict1:
            return [i,dict1[arr[i]]]
        else:
            dict1[a]=i
def majorityElement(arr):
    count=0
    element=1
    for i in range(len(arr)):
        if count==0:
            count+=1
            element=arr[i]
        elif element==arr[i]:
            count+=1
        else:
            count-=1
    if count>=len(arr)//2:
        return element

def maximumSubarraySum(arr):
    max_so_far=float("-inf")
    max_ending=0
    for i in range(len(arr)):
        max_ending=max_ending+arr[i]
        if max_so_far<max_ending:
            max_so_far=max_ending
        if max_ending<0:
            max_ending=0
    return max_so_far
def spiralOrder(matrix):
        m=len(matrix)
        n=len(matrix[0])
        top=0
        down=m-1
        left=0
        right=n-1
        dirs=0
        result=[]
        while(top<=down and left<=right):
            if dirs==0:
                for i in range(left,right+1):
                    result.append(matrix[top][i])
                top+=1
            elif dirs==1:
                for i in range(top,down+1):
                    result.append(matrix[i][right])
                right-=1
            elif dirs==2:
                for i in range(right,left-1,-1):
                    result.append(matrix[down][i])
                down-=1
            elif dirs==3:
                for i in range(down,top-1,-1):
                    result.append(matrix[i][left])
                left+=1
            dirs=(dirs+1)%4
        return result
def spiralOrder1(u):
    matrix = [[0] * u for _ in range(u)]
    top=0
    left=0
    down=u-1
    right=u-1
    n=1
    dirs=0
    while( top<=down and left<=right):
        if dirs==0:
            for i in range(left,right+1):
                matrix[top][i]=n
                n+=1
            top+=1
        
        elif dirs==1:
            for i in range(top,down+1):
                matrix[i][right]=n
                n+=1
            right-=1
        elif dirs==2:
            for i in range(right,left-1,-1):
                matrix[down][i]=n
                n+=1
            down-=1
        elif dirs==3:
            for i in range(down,top-1,-1):
                matrix[i][left]=n
                n+=1
            left+=1
        dirs=(dirs+1)%4
        if n>u*u:
            return matrix
    return matrix
print(spiralOrder1(3))