 def solve(self,start,target,memo):
        if start==target:
            return True
        if "".join(start) in memo:
            return memo[start]
        for i in range(len(start)):
            if start[i]=='L' and i>0 and start[i-1]=='_':
                start[i],start[i-1]=start[i-1],start[i]
                if self.solve(start,target,memo):
                    return True
                start[i-1],start[i]=start[i],start[i-1]
               
            if start[i]=='R' and i<len(start)-1 and start[i+1]=='_':
                start[i],start[i+1]=start[i+1],start[i]
                if self.solve(start,target,memo):
                    return True
                start[i+1],start[i]=start[i],start[i+1]
        memo["".join(start)]=False
        return memo["".join(start)]
def canChange(self, start, target):
    if len(target)!=len(start):
        return False
    i=0
    j=0
    while i<len(start) and j<len(target):
        while i<len(start) and start[i]=='_':
            i+=1
        while j<len(target) and target[j]=='_':
            j+=1
        if i==len(start) or j==len(target) :
            if i==len(start) and j==len(target):
                return True
            return False
        if target[j]!=start[i]:
            return False
        elif start[i]=='L' and i<j:
            return False
        elif start[i]=='R' and i>j:
            return False
        i+=1
        j+=1
    return True
        # start=list(start)
        # target=list(target)
        # memo={}
        # return self.solve(start,target,memo)
    # def maxCount(self, banned, n, maxSum):
        count=0
        sums=0
        for j in range(1,n+1):
            if j in banned:
                continue
            elif maxSum>sums+j:
                count+=1
                sums+=j
            else:
                break
        return count
    def lastStoneWeight(self, stones):
        heap=[]
        for value in stones:
            heap.append(-value)
        heapify(heap)
        while len(heap)>1:
            a=heappop(heap)
            b=heappop(heap)
            if a==b:
                continue
            if a!=b:
                c=(-1*a)-(-1*b)
                heappush(heap,-c)
        return heap[0]*-1
    # def lastStoneWeight(self, stones):