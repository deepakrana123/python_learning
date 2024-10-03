# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
# class Solution:
#     def rotateRight(self, head, k):
#         if not head or not head.next or k == 0:
#             return head
#         temp=head
#         totalLength=0
#         while temp:
#             totalLength+=1
#             temp=temp.next
#         remaingTraversal=totalLength-k%totalLength
#         temp.next=head
#         print(head)
# class Solution:
#     def solve(self,i,j,obstacleGrid):
#         if i<0 or i>=len(obstacleGrid) or j<0 or j>=len(obstacleGrid[0]) or obstacleGrid[i][j]==1:
#             return 0
#         if i==len(obstacleGrid)-1 and j==len(obstacleGrid[0])-1:
#             return 1
#         obstacleGrid[i][j]=1
#         right
#         print("hi")
        
#     def uniquePathsWithObstacles(self, obstacleGrid):
#         return self.solve(0,0,obstacleGrid)
        
        
# def minSubarray(nums, p):
#         sums=sum(nums)
#         target=sums%p
#         if target==0:
#               return 0
#         dicts={}
#         dicts[0]=-1
#         curr_sum=0
#         mins=float("inf")
#         for i in range(len(nums)):
#             curr_sum=(curr_sum+nums[i])%p
#             prev=(curr_sum-target +p)%p
#             if prev in dicts:
#                 mins=min(mins,i-dicts[prev])
#             dicts[curr_sum]=i
#         return mins if mins !=float('inf') else -1
# print(minSubarray([1,2,3],7))



# class Solution:
#     def solve(self,i,j,obstacleGrid):
#         if obstacleGrid[i][j]:
#             return 0
#         if i<0 or j<0 :
#             return 0
#         if i==0 and j==0:
#             return 1
#         right=self.solve(i,j-1,obstacleGrid)
#         down=self.solve(i-1,j,obstacleGrid)
#         return right+down

        
#     def uniquePathsWithObstacles(self, obstacleGrid):
#         self.result=[]
#         return self.solve(len(obstacleGrid)-1,len(obstacleGrid[0])-1,obstacleGrid,)
#         # return self.result
# a=Solution()
# print(a.uniquePathsWithObstacles([[0,0,0],[0,1,0],[0,0,0]]))
from collections import Counter
# class Solutions:
#     def isAnagram(self, s: str, t: str) -> bool:
#         dicts={}
#         for i in range(len(s)):
#             if s[i] in dicts:
#                 dicts[s[i]]+=1
#             dicts[s[i]]=1
#         print(dicts)
#         for i in range(len(t)):
#             if t[i] in dicts:
#                 dicts[t[i]]-=1
#                 if dicts[t[i]]==0:
#                     del dicts[t[i]]
#             else:
#                 return False
#         print(dicts)
#         return len(dicts)==0
# ab=Solutions()
# print(ab.isAnagram(s="a",t="ab"))
# class Solution:
#     def solve(self,prices,index,flag,dp):
#         if index >= len(prices) :
#             return 0
#         taken=0
#         not_taken=0
#         if flag:
#             taken=-prices[index]+self.solve(prices,index,False,dp)
#             not_taken=self.solve(prices,index+1,True,dp)
#         else:
#             taken=prices[index]+self.solve(prices,index+1,True,dp)
#             not_taken=self.solve(prices,index+1,False,dp)
#         return max(taken,not_taken)
#     def maxProfit(self, prices):
#         dp={}
#         return self.solve(prices,0,True,dp)
# a=Solution()
# print(a.maxProfit([1,2,3,4,5]))
class Solution:
    def longestConsecutive(self, nums):
        nums.sort()
        count=1
        curr_num=nums[0]
        for i in range(1,len(nums)):
            if nums[i]==curr_num+1:
                count+=1
                curr_num=nums[i]
        return count
        counts=Counter(nums)
        print(counts,count)
a=Solution()
print(a.longestConsecutive( [0,3,7,2,5,8,4,6,0,1]))
        