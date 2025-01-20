def wordSubsets(words1, words2):
    def isSubSet(freq,temp):
        for i in range(26):
            if temp[i]<freq[i]:
                return False
        return True
    freq=[0]*26
    for word in words2:
        temp=[0]*26
        for w in word:
            temp[ord(w)-ord('a')]+=1
            freq[ord(w)-ord('a')]=max(freq[ord(w)-ord('a')],temp[ord(w)-ord('a')])
    result=[]
    for word in words1:
        temp=[0]*26
        for ch in word:
            temp[ord(ch)-ord('a')]+=1
        if isSubSet(freq,temp):
            result.append(word) 
    return result       
def canConstruct(s, k):
    dicts={}
    if len(s)==k:
        return True
    if len(s)<k:
        return False
    for ch in s:
        dicts[ch]=dicts.get(ch,0)+1
    countOddChar=0
    for ch in dicts:
        if dicts[ch]%2!=0:
            countOddChar+=1
    return countOddChar<=k
def findThePrefixCommonArray(A, B):
    abc=[0]*len(A)
    count=0
    dicts={}
    for i in range(len(A)):
        dicts[B[i]]=dicts.get(B[i],0)+1
        dicts[A[i]]=dicts.get(A[i],0)+1
        if A[i]==B[i] and dicts[A[i]]==2:
            count+=1
        else:
            if dicts[A[i]]==2:
                count+=1
            if dicts[B[i]]==2:
                count+=1
        abc[i]=count
    return abc
def minimumLength(s):
    dicts={}
    for i in range(len(s)):
        dicts[s[i]]=dicts.get(s[i],0)+1
        if dicts[s[i]]==3:
            dicts[s[i]]-=2
    count=0
    for key in dicts:
        count+=dicts[key]
    return count
def canBeValid(s, locked):
    open=[]
    openClose=[]
    i=0
    if len(s)%2!=0:
        return False
    while i <len(s):
        if locked[i]=='0':
            openClose.append(i)
        if locked[i]=='1':
            if s[i]=='(':
                open.append(i)
            elif s[i]==')':
                if open:
                    open.pop()
                elif openClose:
                    openClose.pop()
                else:
                    return False
        i+=1
    while open and openClose and open[-1]<openClose[-1]:
        open.pop()
        openClose.pop()
    return len(open)==0
def isValid(mid,a,n):
    queue=[]
    visited=[False]*n
    queue.append(0)
    visited[0]=True
    while queue:
        u=queue.pop()
        for v,w in a[u]:
            if w != mid and visited[v]==False:
                visited[v]=True
                queue.append(v)
    print(visited,mid)
    for v in visited:
        if v==False:
            return False
    return True
def minMaxWeight(n, edges, threshold):
    a={i:[] for i in range(n)}
    minWeight=0
    maxWeight=float('-inf')
    result=float('inf')
    for u,v,w in edges:
        maxWeight = max(w,maxWeight)
        a[v].append((u,w))
    while minWeight<= maxWeight:
        mid = minWeight + (maxWeight - minWeight)//2
        if isValid(mid,a,n):
            result = mid
            maxWeight = mid-1
        else:
            minWeight = mid+1
    return result if result!=float('inf') else -1
def minimizeXor(num1, num2):
    def isSet(x,bit):
        return (x & (1<<bit) !=0)
    def setBit(x,bit):
        return x |(1<<bit)
    def unsetBit(x,bit):
        return  x&~(1<<bit)
    x=num1
    requriedCount=bin(num2).count('1')
    currentCount=bin(num1).count('1')
    bit=0
    if currentCount<requriedCount:
        while currentCount<requriedCount:
            if not isSet(x,bit):
                setBit(x,bit)
                currentCount+=1
            bit+=1
    elif currentCount>requriedCount:
        while currentCount>requriedCount:
            if isSet(x,bit):
                unsetBit(x,bit)
                currentCount+=1
            bit+=1
    return x
from heapq import heapify, heappush, heappop
def longestConsecutive(nums):
        # if len(nums)==0:
        #     return 0
        # nums.sort()
        # count=0
        maxValue=1
        # for i in range(1,len(nums)):
        #     if nums[i-1]+1==nums[i]:
        #         count+=1
        #     else:
        #         count=0
        #     maxValue=max(maxValue,count)
        # return maxValue+1
        if not nums:
            return 0
        heap=[]
        heapify(heap)
        for i in range(len(nums)):
            heappush(heap,nums[i])
        count=1
        prev=heappop(heap)
        while heap:
            curr=heappop(heap)
            if curr==prev+1:
                count+=1
            elif curr!=prev:
                count=1
            maxValue=max(maxValue,count)
            prev=curr
        return maxValue
        
def longestContinuousSubstring(s):
    count=1
    maxValue=1
    i=1
    prev=s[0]
    while i<len(s):
        if ord(prev)-ord('a')+1==ord(s[i])-ord('a'):
            count+=1
        elif ord(prev)-ord('a')+1!=ord(s[i])-ord('a'):
            count=1
        maxValue=max(maxValue,count)
        prev=s[i]
        i+=1
    return maxValue
def check(nums1,nums2,x):
    j=0
    deleted=0
    i=0
    while i<len(nums1):
        if nums2[j]-nums1[i]!=x:
            deleted+=1
        else:
            j+=1
        i+=1
    if deleted>2:
        return False
    return True
            

def minimumAddedInteger(nums1, nums2):
    nums1.sort()
    nums2.sort()
    minValue=float('inf')
    for num in [[nums2[0]-nums1[0]],[nums2[0]-nums1[1]],nums2[0]-nums1[2]]:
        j=0
        deleted=0
        i=0
        while i<len(nums1):
            if nums2[j]-nums1[i]!=num:
                deleted+=1
            else:
                j+=1
            i+=1
            if deleted>2:
                break
        
    return minValue
# def minOperations(nums, k):
#     if len(nums)==2:
#         return -1
#     heapify(nums)
#     ans=0
#     num=heappop(nums)
#     while num<k:
#         next=2*num+heappop(nums)
#         heappush(nums,next)
#         num=heappop(nums)
#         ans+=1
#     return ans
       
# def xorAllNums(nums1, nums2):
#     m=len(nums1)
#     n=len(nums2)
#     dicts={}
#     for num in nums1:
#         dicts[num]=dicts.get(num,0)+n
#     for num in nums2:
#         dicts[num]=dicts.get(num,0)+m
#     xor=0
#     for key in dicts:
#         if dicts[key]%2 !=0:
#             xor^=key
#     return xor
    
def trapRainWater(heightMap):
    m=len(heightMap)
    n=len(heightMap[0])
    heapQueue=[]
    visited=set()
    if m<3 and n<3:
        return 0
    for i in range(m):
        for v in [0,n-1]:
            heappush(heapQueue,(heightMap[i][v],i,v))
            visited.add((i,v))
    for i in range(n):
        for v in [0,m-1]:
            heappush(heapQueue,(heightMap[v][i],v,i))
            visited.add((v,i))
    water=0
    dir=[[-1,0],[0,1],[1,0],[0,-1]]
    while heapQueue:
        a=heappop(heapQueue)
        currHeight,x,y=a
        for dirs in dir:
            new_x=dirs[0]+x
            new_y=dirs[1]+y
            if new_x>=0 and new_y>=0 and new_x<m and new_y<n and (new_x,new_y) not in visited:
                water+=max(currHeight-heightMap[new_x][new_y],0)
                newHeight=max(currHeight,heightMap[new_x][new_y])
                heappush(heapQueue,(newHeight,new_x,new_y))
                visited.add((new_x,new_y))
    return water


def firstCompleteIndex(arr, mat):
    dicts={arr[i]: i for i in range(len(arr))}
    minIndex=float("inf")
    for i in range(len(mat)):
        c=0
        for j in range(len(mat[0])):
            c=max(dicts[mat[i][j]],c)
        minIndex=min(minIndex,c)
    for j in range(len(mat[0])):
        c=0
        for i in range(len(mat)):
            c=max(dicts[mat[i][j]],c)
        minIndex=min(minIndex,c)
    return minIndex
def highestPeak(isWater):
    queue=[]
    m=len(isWater)
    n=len(isWater[0])
    result=[[-1 for _ in range(len(isWater[0]))] for _ in range(len(isWater))]
    for i in range(len(isWater)):
        for j in range(len(isWater[0])):
            if isWater[i][j]==1:
                result[i][j]=0
                queue.append((i,j))
    dirs=[[-1,0],[0,1],[1,0],[0,-1]]
    while queue:
        k=len(queue)
        for _ in range(k):
            x,y=queue.pop(0)
            for d in dirs:
                curr_x = x+d[0]
                curr_y = y + d[1]
                if curr_x>=0 and curr_y>=0 and curr_x<m and curr_y<n and result[curr_x][curr_y] == -1:
                    result[curr_x][curr_y]=result[x][y]+1
                    queue.append((curr_x,curr_y))
            
    return result

            
        


        
        

       

# print(minimumAddedInteger( [4,20,16,12,8],[14,18,10]))
# print(trapRainWater([[1,4,3,1,3,2],[3,2,1,3,2,4],[2,3,3,2,3,1]]))
# print(trapRainWater([[3,3,3,3,3],[3,2,2,2,3],[3,2,1,2,3],[3,2,2,2,3]]))
# print(firstCompleteIndex([1,3,4,2], mat = [[1,4],[2,3]]))
# print(firstCompleteIndex([2,8,7,4,1,3,5,6,9], mat = [[3,2,5],[1,4,6],[8,7,9]]))
print(highestPeak([[0,0,1],[1,0,0],[0,0,0]]))