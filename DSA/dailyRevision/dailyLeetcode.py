from heapq import heappop, heappush, heapify
from collections import deque 
class Solution:
    def __init__(self, k: int, nums):
        self.k=k
        self.heap=[]
        for num in nums:
            heappush(self.heap,-num)
    def add(self, val: int) -> int:
        heappush(self.heap,-val[0])
        return -1*self.heap[self.k-1]
    def kWeakestRows(self, mat, k):
        currheap=[]
        for i in range(len(mat)):
            sums=sum(mat[i])
            heappush(currheap,(sums,i))
        n=0
        a=[]
        while n<k:
            a.append(heappop(currheap)[1])
            n+=1
        return a
    def topKFrequent(self, nums, k):
        dicts={}
        for num in nums:
            dicts[num]=dicts.get(num,0)+1
        currNewHeap=[]
        for key in dicts:
            heappush(currNewHeap,(-dicts[key],key))
        print(currNewHeap)
        newD=[]
        for u,v in currNewHeap:
            newD.append(v)
        return newD[0:k]
    # def maxTwoEvents(self, events):
    #     a=events.sort(key=lambda num:num[0])
    #     print(a,events)
    #     start=0
    #     end=0
    #     result=0
    #     currresult=0
    #     i=0
    #     while i<len(events):
    #         print(start,end,currresult,result)
    #         if end<events[i][0]:
    #             start=events[i][0]
    #             end=events[i][1]
    #             currresult=events[i][2]
    #             result+=currresult
    #         elif start==events[i][0]:
    #             if currresult<events[i][2]:
    #                 result+=events[i][2]-currresult
    #                 currresult=max(currresult,events[i][2])
                
    #         i+=1
    #     return result
    def kSmallestPairs(self, nums1, nums2, k):
        hnoweap=[]
        for i in range(len(nums1)):
            for j in range(len(nums2)):
                heappush(hnoweap,(nums1[i]+nums2[j],nums1[i],nums2[j]))
        result=[]
        while k>0:
            a=heappop(hnoweap)
            result.append([a[1],a[2]])
            k-=1
        return result
    # def frequencySort(self, s):
    #     a={}
    #     for i in range(len(s)):
    #         a[s[i]]=a.get(s[i],0)+1
    #     freHeap=[]
    #     for key in
    def maximumLength(self, s: str) -> int:
        a=[[0 for _ in range(len(s)+1)] for _ in range(26)]
        currChar=""
        for i in range(len(s)):
            if currChar and currChar[-1]==s[i]:
                currChar+=s[i]
                abc=len(currChar)
                a[ord(s[i])-ord('a')][abc]+=1
            else:
                currChar=s[i]
                a[ord(s[i])-ord('a')][1]=1
        result=0
        print(a)
        for i in range(26):
            cuuSumm=0
            for j in range(len(s),0,-1):
                cuuSumm+=a[i][j]
                if cuuSumm>=3:
                    result=max(result,j)
                    break
        return result
    def maximumBeauty(self, nums, k):
        result=[]
        for i in range(len(nums)):
            result.append([nums[i]-k,nums[i]+k])
        result.sort(key=lambda name:name[0])
        maxResult=0
        end=float("inf")
        queue=deque([])
        for i in range(len(result)):
            while queue and  queue[0][1]<result[i][0]:
                queue.popleft()
            queue.append(result[i])
            maxResult=max(maxResult,len(queue))
        return maxResult
#     
a=Solution(3,[4,5,8,2,3,5,10])
# def __init__(self):
#         self.minHeap=[]
#         self.maxHeap=[]
        
#  # def addNum(self, num: int) -> None:
#         heappush(self.maxHeap,-num)
#         if self.maxHeap and self.minHeap and (-self.maxHeap[0]>self.minHeap[0]):
#             heappush(self.minHeap,-heappop(self.maxHeap))
#         if len(self.minHeap)+1<len(self.maxHeap):
#             heappush(self.minHeap,-heappop(self.maxHeap))
#         else:
#             heappush(self.maxHeap,-heappop(self.minHeap))


#     # def findMedian(self) -> float:
#     #     if len(self.maxHeap) > len(self.minHeap):
#     #         return -self.maxHeap[0]
#     #     else:
#     #         return (-self.maxHeap[0] + self.minHeap[0]) / 2.0
#     # def totalCost(self, costs, k, candidates):
#         hired=0
#         ans=0
#         queue1=[]
#         queue2=[]
#         i=0
#         j=len(costs)-1
#         while hired<k:
#             while queue1 and i<=j:
#                 heappush(queue1,costs[i])
#                 i+=1
#             while queue2 and j>=i:
#                 heappush(queue2,costs[j])
#                 j-=1
#             a=queue1[-1] if queue1 else float("inf")
#             b=queue2[-1] if queue2 else float("inf")
#             if a<b:
#                 ans+=a
#                 heappop(queue1)
#             else:
#                 ans+=b
#                 heappop(queue2)
#             hired+=1
#         return ans
    

# print(a.kSmallestPairs([1,1,2], nums2 = [1,2,3], k = 2))
# print(a.frequencySort("tree"))
# print(a.frequencySort('cccaaa'))
# print(a.maximumLength("aaaa"))
# print(a.maximumLength("aaaa"))
# print(a.maximumBeauty([4,6,1,2],2))
import math
class MedianFinder:
    # def maxAverageRatio(self, classes, extraStudents):
    #     heap=[]
    #     for i in range(len(classes)):
    #         heap.append([classes[i][0]/classes[i][1],classes[i][0],classes[i][1]])
    #     k=extraStudents
    #     while heap and k:
    #         a,b,c=heappop(heap)
    #         heappush(heap,[(b+1)/(c+1),b+1,c+1])
    #         k-=1
    #     result=0
    #     while heap:
    #         a,b,c=heappop(heap)
    #         result+=a
    #     return result/len(classes)
    #  def findScore(self, nums):
    #     mp=set()
    #     heap=[]
    #     result=0
    #     for i in range(len(nums)):
    #         heap.append([nums[i],i])
    #     heapq.heapify(heap)
    #     while heap:
    #         a,b=heappop(heap)
    #         if b not in mp:
    #             result+=a
    #             mp.add(b)
    #             if b-1>=0:
    #                 mp.add(b-1)
    #             if b+1<len(nums):
    #                 mp.add(b+1)
    #     return result
    
    def findMaximizedCapital(self, k, w, profits, capital):
        weight=w
        heap=[]
        for i in range(len(capital)):
            capital[i]=[capital[i],profits[i]]
        capital.sort(key=lambda item:item[0])
        i=0
        while k>0:
            while i<len(capital) and capital[i][0]<=weight:
                heappush(heap,-capital[i][1])
                i+=1
            if len(heap)==0:
                break
            a=heappop(heap)
            weight+=-a
            k-=1
        return weight
    # def repeatLimitedString(self,s, repeatLimit):
        # a=[0]*26
        # for num in s:
        #     a[ord(num)-ord('a')]+=1
        # result=""
        # i=len(a)-1
        # j=0
        # while i>=0:
        #     if a[i]==0:
        #         i-=1
        #         continue
        #     ch = chr(ord('a')+i)
        #     freq=min(a[i],repeatLimit)
        #     result+=ch*freq
        #     a[i]-=freq
        #     if a[i]>0:
        #         j=i-1
        #         while j>=0 and a[j]==0:
        #             j-=1
        #         if j<0:
        #             break
        #         ch = chr(ord('a')+j)
        #         result+=ch
        #         a[j]-=1
        # return result
    # def maxChunksToSorted(self, arr):
        # a=[0]*(len(arr))
        # a[0]=0
        # for i in range(1,len(arr)):
        #     a[i]=a[i-1]+i
        # result=0
        # sum=0
        # for i in range(len(arr)):
        #     sum+=arr[i]
        #     if sum==a[i]:
        #         result+=1
        # return result
    # def minStoneSum(self, piles, k):
    #     heap=[]
    #     for num in piles:
    #         heap.append(-num)
    #     heapify(heap)
    #     while k>0:
    #         a=-1*heappop(heap)
    #         heappush(heap,-math.ceil(a/2))
    #         k-=1
    #     s=0
    #     while heap:
    #         a=-1*heappop(heap)
    #         s+=a
    #     return s        
    # def halveArray(self, nums):
    #     max_heap = []
    #     total_sum = sum(nums)
    #     target = total_sum / 2
    #     current_sum = 0
    #     operations = 0
    #     for num in nums:
    #         heappush(max_heap, -num)
    #     while current_sum < target:
    #         largest = -heappop(max_heap)
    #         current_sum += largest / 2
    #         heappush(max_heap, -largest / 2)
    #         operations += 1
    #     return operations
    def minOperations(self, nums, k):
        if len(nums)==2:
            return -1
        heap=[]
        for num in nums:
            heap.append(num)
        operations=0
        while heap:
            a=heappop(heap)
            b=heappop(heap) if heap else 0
            if a>=k or b>=k:
                return operations
            c=min(a,b)*+max(a,b)
            heappush(heap,c)
            operations+=1
        return operations
    # def minimumOperations(self, root):
    #     if root is None:
    #         return []
    #     queue = deque([root])
    #     result=0
    #     while queue:
    #         size=len(queue)
    #         levelNodes=[]
    #         while size:
    #             a=queue.pop()
    #             levelNodes.append(a)
    #             if a.left:
    #                 queue.append(a.left)
    #             if a.right:
    #                 queue.append(a.right)
    #             size-=1
    #         for i in range(len(levelNodes)):
    #             if sorted(levelNodes)[i]!=levelNodes[i]:
    #                 result+=1
    #     return result
    def maxRectangleArea(self, points):
        n=len(points)
        pointSet=set()
        for num in points:
            pointSet.add((num[0],num[1]))
        area=-1
        for i in range(n):
            for j in range(i+1,n):
                x1=points[i][0]
                y1=points[i][1]
                x2=points[j][0]
                y2=points[j][1]
                if x1!=x2 and y1!=y2:
                    if (x1,y2) in pointSet and (x2,y1) in pointSet:
                        calarea=abs(x2-x1)*abs(y2-y1)
                        validRectangle=True
                        for k in range(n):
                            x=points[k][0]
                            y=points[k][1]
                            if ((x==x1 or x==x) and (y==y1 or y==y2)):
                                continue
                            if (x>min(x1,x2) and x < max(x1,x2) and y > min(y1,y2) and y<max(y1,y2)):
                                validRectangle=False
                                break
                            if ((x==x1 or x==x2) and (y>=min(y1,y2) and y <= min(y1,y2))):
                                validRectangle=False
                                break
                            if ((y==y1 or y==y2) and (x>=min(x1,x2) and x <= min(x1,x2))):
                                validRectangle=False
                                break
                        if(validRectangle):
                            area=max(area,calarea)
                        # area=min(calarea,area)
        return area
    def findTargetSumWays(self, nums, target):
        dp={}
        def solve(nums,target,sums,index,dp):
            if index==len(nums):
                if sums==target:
                    return 1
                return 0
            if (sums,index) in dp:
                return dp[(sums,index)]
            plus=solve(nums,target,sums+nums[index],index+1,dp)
            minus=solve(nums,target,sums-nums[index],index+1,dp)
            dp[(sums,index)]=plus+minus
            return dp[(sums,index)]
        return solve(nums,target,0,0,dp)
    def maxScoreSightseeingPair(self, values):
        result=0
        # max1=[0]*len(values)
        # for i in range(len(values)):
        #     max1[i]=values[i]+i
        maxi=values[0]+0
        for j in range(1,len(values)):
            result=max(result,maxi+values[j]-j)
            if values[j]+j>maxi:
                maxi=values[j]+j
        return result
    def vowelStrings(self, words, queries):
        currSum=[0]*len(words)
        count=0
        ans=[]
        for i in range(len(words)):
            if (words[i][0]=='a' or words[i][0]=='e' or words[i][0]=='i' or words[i][0]=='o' or words[i][0]=='u') and (words[i][-1]=='a' or words[i][-1]=='e' or words[i][-1]=='i' or words[i][-1]=='o' or words[i][-1]=='u'):
                count+=1
            currSum[i]=count
        for q in queries:
            l,r=q
            if l>=0:
                if l==0:
                    ans.append(currSum[r])
                else:
                    ans.append(currSum[r]-currSum[l-1])
        return ans
    def licenseKeyFormatting(self, s, k):
        a=s.split('-')
        s1=a[0]
        c=''
        for i in range(0,len(a)):
            for j in range(len(a[i])):
                c+=a[i][j]
                if len(c)==k:
                    s1+='-'+c.upper()
        return s1
    def shiftingLetters(self, s, shifts):
        an=[0]*len(s)
        for i in range(len(shifts)):
            start,end,incre=shifts[i]
            for j in range(start,end+1):
                an[j]+=1 if incre==1 else -1
        s1=''
        for i in range(len(s)):
            new_ord=ord(s[i])+an[i]
            if new_ord<ord('a'):
                new_ord=ord('z')+1+(new_ord-ord('a'))
            elif new_ord>ord('z'):
                new_ord=ord('a')+ (new_ord - ord('a')) % 26
            s1+=chr(new_ord)
        return s1
                
        
        
abc=MedianFinder()
# print(abc.minOperations([1,1,2,4,9], k = 20))
# print(abc.maxRectangleArea([[1,1],[1,3],[3,1],[3,3]]))
# print(abc.maxRectangleArea(  [[1,1],[1,3],[3,1],[3,3],[1,2],[3,2]]))
# print(abc.findTargetSumWays([1,1,1,1,1],3))
# print(abc.maxScoreSightseeingPair([8,1,5,2,6]))
# print(abc.maxScoreSightseeingPair([1,2]))
# print(abc.triangleNumber([4,2,3,4]))
# print(abc.vowelStrings(["a","e","i"], queries = [[0,2],[0,1],[2,2]]))
# print(abc.licenseKeyFormatting( "2-5g-3-J", k = 2))
print(abc.shiftingLetters("xuwdbdqik", shifts = [[4,8,0],[4,4,0],[2,4,0],[2,4,0],[6,7,1],[2,2,1],[0,2,1],[8,8,0],[1,3,1]]))
