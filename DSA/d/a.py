# class Solution:
#     def convertDateToBinary(self,date):
#         s=date.split('-')
#         a=""
#         for i in range(len(s)):
#             if s[i][0]=='0':
#                 a+=bin(int(s[i][1:]))[2:]+'-'
#             else:
#                 a+=bin(int(s[i]))[2:]+'-'
#         return a[0:len(a)-1].lstrip('0')
# a=Solution()
# print(a.convertDateToBinary("2080-02-29"))    
# class Solution:
#     def minBitFlips(self,start, goal,c):
#         xor_result = start ^ goal
#         xor_result1 = xor_result ^ c
#         print(xor_result,xor_result1)
#         count = 0
#         while xor_result1 > 0:
#             count += xor_result1 & 1
#             xor_result1 >>= 1
        
#         return count
        

# a=Solution()
# print(a.minBitFlips(2,6,5))
# class Solution:
#     def minOperations(self, nums):
#         count=0
#         for i in range(1,len(nums)):
#             count+=abs(max(nums[i],nums[i-1]+1)-nums[i])
#             nums[i]=max(nums[i],nums[i-1]+1)
#         return count
# a=Solution()
# print(a.minOperations([1,1,1]))
# import heapq
# class Solution:
#     def maximumProduct(self, nums, k):
#         p=pow(10,9)+7
#         heapq.heapify(nums)
#         while k>0:
#             heapq.heappush(nums,heapq.heappop(nums)+1)
#             k-=1
#         a=1
#         for x in nums:
#             a=(x*a)%p
#         return a
# a=Solution()
# print(a.maximumProduct( [6,3,3,2], k = 2))
class Solution:
    def findMaximumNumber(self, k: int, x: int) -> int:
        def count_set_bits(n,x):
            count = 0
            while n >0:
                count+=n&1
                n >>= x
            return count
        sums=0
        for i in range(1,k+1):
            sums+=count_set_bits(i,x)
            if sums==k:
                return i
            
a=Solution()
print(a.findMaximumNumber(9,1))




        
        
        
            
            
        
        
        
            
        
        