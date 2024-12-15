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
import heapq
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
     def findScore(self, nums):
        mp=set()
        heap=[]
        result=0
        for i in range(len(nums)):
            heap.append([nums[i],i])
        heapq.heapify(heap)
        while heap:
            a,b=heappop(heap)
            if b not in mp:
                result+=a
                mp.add(b)
                if b-1>=0:
                    mp.add(b-1)
                if b+1<len(nums):
                    mp.add(b+1)
        return result

        
abc=MedianFinder()
print(abc.findScore([2,1,3,4,5,2]))
# print(abc.maxAverageRatio( [[2,4],[3,9],[4,5],[2,10]], extraStudents = 4))