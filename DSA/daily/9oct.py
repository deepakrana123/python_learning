# class Solution:
#     def finalPrices(self, prices):
#         for i in range(len(prices)):
#             for j in range(i+1,len(prices)):
#                 if prices[j]<=prices[i]:
#                     prices[i]=prices[i]-prices[j]
#                     break
#                 else:
#                     prices[i]=prices[i]
#         return prices
# a=Solution()
# print(a.finalPrices([8,4,6,2,3]))
# print(a.finalPrices([1,2,3,4,5]))
# print(a.finalPrices([10,1,1,6]))
# class Solution:
#     def minOperations(self, nums, k):
#         dicts={}
#         for i in range(1,k+1):
#             dicts[i]=dicts.get(i,0)+1
#         operations=0
#         for i in range(len(nums)-1,-1,-1):
#             if nums[i] in dicts:
#                 dicts[nums[i]]=dicts[nums[i]]-1
#                 if dicts[nums[i]]==0:
#                     del dicts[nums[i]]
#             operations+=1
#             if len(dicts)==0:
#                 return operations

# a=Solution()
# print(a.minOperations([3,2,5,3,1], k = 3))
from collections import Counter
import heapq
class Solution:
    def reorganizeString(self, s):
        d=Counter(s)
        heap = []
        for key,val in d.items():
            if val!=0:
                heap.append((-val,key))
        heapq.heapify(heap)
        strs=""
        while len(heap)>1:
            first, char1 = heapq.heappop(heap)
            second, char2 = heapq.heappop(heap)
            strs+=char1
            strs+=char2
            if first+1 < 0:
                heapq.heappush(heap, (first+1, char1))
            if second +1< 0:
                heapq.heappush(heap, (second+1, char2)) 
        if heap:
            last,charlast=heapq.heappop(heap)
            if last==-1:
                strs += last[1]
            else:return ""
        return strs

a=Solution()
print(a.reorganizeString("aab"))
 
        
        