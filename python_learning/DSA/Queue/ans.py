from collections import deque


def kth_size_neg_num(arr, k):
    queue = deque()
    ans = []
    # process first window of k size
    for i in range(k):
        if (arr[i] < 0):
            queue.append(i)
    if queue:
        ans.append(queue[0])
    else:
        ans.append(0)
    for i in range(k, len(arr)):
        if queue and i-queue[0] >= k:
            queue.popleft()
    if arr[i] < 0:
        queue.append(i)
    if queue:
        ans.append(queue[0])
    else:
        ans.append(0)
    return ans

def reverseFirstKElement(arr,k):
    a=[]
    queue = deque()
    n=len(a)
    for i in range(len(arr)):
        queue.append(arr[i])
    for i in range(k):
        a.append(queue.popleft())
    while a:
        queue.append(a.pop())
    for i in range(n-k,-1,-1):
        queue.append(queue.popleft)
    return queue

def firstNonRepeatingCharcater(s):
    m={}
    queue=deque()
    ans=[]
    for i in range(len(s)):
        if m[s[i]]:
            m[s[i]]+=1
        else:
            m[s[i]]=1
        queue.append(s[i])
    
    while queue:
        if(m[queue[0]]>1):
            queue.popleft()
        else:
            ans.append(queue[0])
            break
    if len(q)==0:
        ans.append("#")
        
    return ans
        

    
    
    
