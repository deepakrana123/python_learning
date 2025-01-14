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

        
    
        
# print(canConstruct("true", k = 4))
# print(wordSubsets(["amazon","apple","facebook","google","leetcode"], words2 = ["e","o"]))
# print(wordSubsets(["amazon","apple","facebook","google","leetcode"], words2 = ["lc","eo"]))
# print(findThePrefixCommonArray([2,3,1], B = [3,1,2]))
# print(findThePrefixCommonArray([1,3,2,4], B = [3,1,2,4]))
# print(minimumLength("abaacbcbb"))
# print(canBeValid("))()))", locked = "010100"))
print(minMaxWeight( 5, edges = [[1,0,1],[2,0,2],[3,0,1],[4,3,1],[2,1,1]], threshold = 2))
