def longestIdealString(s, k):
    arr=[0]*26
    result=0
    for i in range(len(s)):
        curr=ord(s[i])-ord('a')
        left=max(0,curr-k)
        right=min(26,curr+k)
        longest=0
        for j in range(left,right+1):
            longest=max(longest,arr[j])
        arr[curr]=max(arr[curr],longest+1)
        result=max(result,arr[curr])
    return result

def longestIdealString1(s,k):
    result=[0]*len(s)
    for i in range(len(s)):
        for j in range(len(s)):
            if abs(ord(s[i])-ord(s[j]))<=k:
                t[i]
                

# class Solution:
#     def solve(self,nums,index,previous,dp):
#         if index == len(nums):
#             return 0
#         if dp[index][previous+1]!=-1:
#             return dp[index][previous+1]
#         skip = 0 + self.solve(nums,index+1,previous,dp)
#         take=0
#         if previous == -1 or nums[previous]<nums[index]:
#             take = 1 + self.solve(nums,index+1,index,dp)
#         dp[index][previous+1] = max(skip,take)
#         return dp[index][previous+1]           
#     def lengthOfLIS(self, s: str, k: int) -> int:
#         dp=[[-1 for j in range(len(nums)+1)] for i in range(len(nums))]
#         return self.solve(0,-1,nums,dp)