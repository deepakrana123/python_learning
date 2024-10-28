# from collections import Counter
# class Solution:
#     def findAnagrams(self, s, p):
#         i=0
#         j=0
#         arr=[]
#         strs={}
#         count=Counter(p)
#         while j<len(s):
#             strs[s[j]]=strs.get(s[j],0)+1
#             if count==strs:
#                 arr.append(i)
#             while len(strs)>=len(count) and count!=strs:
#                 strs={} 
#                 i=j
#             j+=1
#         return arr
# a=Solution()
# print(a.findAnagrams("cbaebabacd", "abc"))



# import heapq
# class Solution:
#     def findKthNumber(self, m, n, k):
#         # min_heap=[]
#         # heapq.heapify(min_heap)
#         # i=1
#         # j=1
#         # while i<=m:
#         #     heapq.heappush(min_heap,i*j)
#         #     j+=1
#         #     if j>n:
#         #         j=1
#         #         i+=1
#         # a=-1
#         # while k>0:
#         #     a = heapq.heappop(min_heap)
#         #     k-=1
#         # return a
#         a=[[-1 for _ in range(n)] for _ in range(m)]
#         for i in range(m):
#             for j in range(n):
#                 a[i][j]=i*j
        
# a=Solution()
# print(a.findKthNumber(2,3,6))

# class Solution:
#     def kthSmallest(self, matrix, k):
#         rowCount = len(matrix)
#         min_heap = []
#         for i in range(min(rowCount, k)):
#             heapq.heappush(min_heap, (matrix[i][0], i, 0))
#         numbers_checked = 0
#         smallest_element = 0
#         while min_heap:
#             smallest_element, row_index, col_index = heapq.heappop(min_heap)
#             numbers_checked += 1
#             if numbers_checked == k:
#                 break
#             if col_index + 1 < len(matrix[row_index]):
#                 heapq.heappush(min_heap, (matrix[row_index][col_index + 1], row_index, col_index + 1))
#                 print(min_heap)
        
#         return smallest_element
            
        
# a=Solution()
# print(a.kthSmallest([[1,5,9],[10,11,13],[12,13,15]],8))
        



# class Solution:
#     def xorQueries(self, arr, queries):
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
# class Solution:
#     def findHeight(self,root,level):
#         if root is None:
#             return 0
#         self.levelOrder[root.val]=level
#         self.height[root.val]=max(self.findHeight(root.right,level+1),self.findHeight(root.left,level+1))
#         if self.maxHeight[self.level]< self.height[root.val]:
#             self.secondMaxHeight[self.level]= self.maxHeight[self.level]
#             self.maxHeight[self.level]=self.height[root.val]
#         elif self.secondMaxHeight[self.level]<self.height[root.val]:
#             self.secondMaxHeight[self.level]=self.height[root.val]
        
#         return self.height[root.val]
            
        
#     def treeQueries(self, root, queries):
#         self.levelOrder=[0]*1000001
#         self.height=[0]*1000001
#         self.maxHeight=[0]*1000001
#         self.secondMaxHeight=[0]*1000001
#         self.findHeight(root,0)
#         result=[0]*len(queries)
#         for nodes in queries:
#             l=self.levelOrder[nodes]
#             if self.levelOrder[l]== self.height[l]:
#                 temp=l+ self.secondMaxHeight[l]
#             else:
#                 temp=l+ self.maxHeight[l]-1
#             result.append(temp)
#         return result
        
        
        
        
# import math
# class Solution:
#     def longestSquareStreak(self,nums):
#         nums.sort()
#         dicts={}
#         maxStreak=-1
#         for num in nums:
#             qa=math.sqrt(num)
#             if qa*qa==num and qa in dicts:
#                 dicts[num]=dicts[qa] + 1
#                 maxStreak=max(maxStreak,dicts[qa] + 1)
#             else:
#                 dicts[num]=1
#         return -1 if maxStreak < 2 else maxStreak
        
# a=Solution()
# print(a.longestSquareStreak([4,3,6,16,8,2]))
# print(a.longestSquareStreak([2,3,5,6,7]))
class Solution:
    def removeSubfolders(self, folder):
        dicts=[]
        for num in folder:
            isSubFolder=False
            currFolder = num
            while dicts and currFolder:
                res = len(currFolder) - 1 - currFolder[::-1].index('/')
                currFolder = currFolder[0:res]
                print(currFolder,dicts,"curFolder")
                if currFolder in dicts:
                    isSubFolder=True
                    break
            if isSubFolder ==False:
                dicts.append(num)    
        return dicts
a=Solution()
print(a.removeSubfolders( ["/ad","/ad/af","/aa"]))
        