# # # class Solution:
# # #     def convertDateToBinary(self,date):
# # #         s=date.split('-')
# # #         a=""
# # #         for i in range(len(s)):
# # #             if s[i][0]=='0':
# # #                 a+=bin(int(s[i][1:]))[2:]+'-'
# # #             else:
# # #                 a+=bin(int(s[i]))[2:]+'-'
# # #         return a[0:len(a)-1].lstrip('0')
# # # a=Solution()
# # # print(a.convertDateToBinary("2080-02-29"))    
# # # class Solution:
# # #     def minBitFlips(self,start, goal,c):
# # #         xor_result = start ^ goal
# # #         xor_result1 = xor_result ^ c
# # #         print(xor_result,xor_result1)
# # #         count = 0
# # #         while xor_result1 > 0:
# # #             count += xor_result1 & 1
# # #             xor_result1 >>= 1
        
# # #         return count
        

# # # a=Solution()
# # # print(a.minBitFlips(2,6,5))
# # # class Solution:
# # #     def minOperations(self, nums):
# # #         count=0
# # #         for i in range(1,len(nums)):
# # #             count+=abs(max(nums[i],nums[i-1]+1)-nums[i])
# # #             nums[i]=max(nums[i],nums[i-1]+1)
# # #         return count
# # # a=Solution()
# # # print(a.minOperations([1,1,1]))
# # # import heapq
# # # class Solution:
# # #     def maximumProduct(self, nums, k):
# # #         p=pow(10,9)+7
# # #         heapq.heapify(nums)
# # #         while k>0:
# # #             heapq.heappush(nums,heapq.heappop(nums)+1)
# # #             k-=1
# # #         a=1
# # #         for x in nums:
# # #             a=(x*a)%p
# # #         return a
# # # a=Solution()
# # # print(a.maximumProduct( [6,3,3,2], k = 2))
# # # class Solution:
# # #     def findMaximumNumber(self, k: int, x: int) -> int:
# # #         def count_set_bits(n,x):
# # #             count = 0
# # #             while n >0:
# # #                 count+=n&1
# # #                 n >>= x
# # #             return count
# # #         sums=0
# # #         for i in range(1,k+1):
# # #             sums+=count_set_bits(i,x)
# # #             if sums==k:
# # #                 return i
            
# # # a=Solution()
# # # print(a.findMaximumNumber(9,1))
# # class Solution:
# #     def smallestRangeII(self,nums, k):
# #         nums.sort()
# #         arr1=[0]*len(nums)
# #         arr2=[0]*len(nums)
# #         for i in range(len(nums)):
# #             arr1[i]=nums[i]-k if nums[i]-k>0 else 0
# #             arr2[i]=nums[i]+k
# #         minmax1=min(arr1)
# #         minmax2=max(arr1)
# # a=Solution()
# # print(a.smallestRangeII([1,3,6], k = 3))
        
# # Definition for a binary tree node.
# # class TreeNode:
# #     def __init__(self, val=0, left=None, right=None):
# #         self.val = val
# #         self.left = left
# #         self.right = right
# # class Solution:
# #     def getHeight(self,root,h):
# #         print
# #         if root==None:
# #             return h
# #         self.getHeight(root.left,h+1)
# #     def getRightHeight(self,root,h):
# #         if root==None:
# #             return h
# #         self.getRightHeight(root.right,h+1)
# #     def isBalanced(self, root) -> bool:
# #         if root == None: return True
# #         lh=self.getHeight(root,0)
# #         lr=self.getRightHeight(root,0)
# #         print(lh,lr)
# #         return lr-lh==1

# # class Solution:
# #     def xorQueries(self, arr, queries):
# #         a=[0]*(len(arr)+1)
# #         for i in range(1,len(arr)+1):
# #             a[i]=a[i-1]^arr[i-1]
# #         ans=[]
# #         for l,r in queries:
# #             ans.append(a[l]^a[r+1])
# #         return ans



# # a=Solution()
# # print(a.xorQueries([1,3,4,8], queries = [[0,1],[1,2],[0,3],[3,3]]
# # ))
# # class Solution:
# #     def countSegments(self, s: str) -> int:
# #         a=[]
        
# # a=Solution()
# # print(a.countSegments("Hello, my name is John"))
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
# class Solution:    
#     def __init__(self):
#         root=TreeNode()
#     def getHeight(self,root):
#         if root==None:
#             return 0
#         lh=self.getHeight(root.left)
#         lr=self.getHeight(root.right)
#         if lh==-1 or lr==-1:return -1
#         if abs(lr-lh)>1:return -1
#         return max(lh,lr)+1
#     def isBalanced(self, root: Optional[TreeNode]) -> bool:
#         if root == None: return True
#         if self.getHeight(root)==-1: return False
#         return True
        
        
        
             




        
        
class Solution:
    def findSafeWalk(self, grid, health):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        queue=[(0,0,health)]
        visited=set()
        visited.add((0,0,health))
        i=0
        j=0
        m=len(grid)
        n=len(grid[0])
        while queue:
            i,j,curr_health=queue.pop(0)
            if i==m-1 and j==n-1 and curr_health>=1:
                return True
            for di, dj in directions:
                ni, nj = i + di, j + dj
                if 0 <= ni < m and 0 <= nj < n:
                    print(ni,nj,i,j)
                    newHealth = curr_health-grid[ni][nj]
                    if newHealth > 0 and (ni, nj, newHealth) not in visited:
                        visited.add((ni, nj, newHealth))
                        queue.append((ni, nj, newHealth))
        print(visited)
        return False
            
a=Solution()
print(a.findSafeWalk([[1,1,1,1]],4))
        
        
        
            
        
        