# class Solution:
#     def smallestRange(self, nums):
#         k = len(nums)
#         pointers = [0] * k
#         result = [float('-inf'), float('inf')]
#         while True:
#             current_min = float('inf')
#             current_max = float('-inf')
#             min_list_index = -1
#             for i in range(k):
#                 if pointers[i] >= len(nums[i]):
#                     return result if result[0] != float('-inf') else []
#                 current_num = nums[i][pointers[i]]
#                 if current_num < current_min:
#                     current_min = current_num
#                     min_list_index = i
#                 if current_num > current_max:
#                     current_max = current_num
#             if current_max - current_min < result[1] - result[0]:
#                 result = [current_min, current_max]
#             pointers[min_list_index] += 1
#             if pointers[min_list_index] >= len(nums[min_list_index]):
#                 break
        
#         return result
# a=Solution()
# print(a.smallestRange([[4,10,15,24,26],[0,9,12,20],[5,18,22,30]]))
        

# from heapq import heappop, heappush, heapify
# class Solution:
#     def minGroups(self, intervals):
#         intervals.sort(key=lambda item:item[0])
#         heap = []
#         heapify(heap)
#         for interval in intervals:
#             start,end=interval
#             if heap and start>heap[0]:
#                 heappop(heap)
#             heappush(heap,end)
#         return len(heap)
        
# a=Solution()
# print(a.minGroups([[5,10],[6,8],[1,5],[2,3],[1,10]]))
# class Solution:
#     def maximumSwap(self, num: int) -> int:
#         aa=str(num)
#         a=[]
#         for nums in aa:
#             a.append(nums)
#         for i in range(1,len(a)):
#             if a[i]>a[i-1]:
#                 a[i-1],a[i]=a[i],a[i-1]
#                 break
#         return int(''.join(a))



        
# a=Solution()
# print(a.maximumSwap(9973))
# class Solution:
#     def maximumSwap(self, num: int) -> int:
#         aa=str(num)
#         a=[]
#         for nums in aa:
#             a.append(nums)
#         for i in range(1,len(a)):
#             if a[i]>a[i-1]:
#                 a[i-1],a[i]=a[i],a[i-1]
#                 break
#         return int(''.join(a))
# class Solution:
#     def solve(self,nums,index,currOr):
#         if index>=len(nums):
#             if currOr==self.maxOr:
#                 return 1
#             return 0
#         taken=self.solve(nums,index+1,currOr | nums[index])
#         notTaken=self.solve(nums,index+1,currOr)
#         return taken+notTaken
#     def countMaxOrSubsets(self, nums):
#         self.maxOr=1
#         for num in nums:
#             self.maxOr|=num
#         return self.solve(nums,0,1)
# a=Solution()
# print(a.countMaxOrSubsets([2,2,2]))
# class Solution:
#     def findKthBit(self, n: int, k: int) -> str:
#         if n==1:
#             return "0"
#         length=(1<<n)-1
#         print(length,n)
#         if k < length//2:
#             return self.findKthBit(n-1,k)
#         elif k == length//2:
#             return "1"
#         else:
#             ch=self.findKthBit(n-1,length-(k-1))
#             return "0" if ch=="1" else "0"        
# a=Solution()
# print(a.findKthBit(3,1))
# class Solution:
#     def operatorValues(self, values, operator):
#         if operator == '!':
#             return 'f' if values[0] == 't' else 't'
#         if operator == '&':
#             for value in values:
#                 if value == 'f':
#                     return 'f'
#             return 't'
#         if operator == '|':
#             for value in values:
#                 if value == 't':
#                     return 't'
#             return 'f'
#     def parseBoolExpr(self, expression):
#         n=len(expression)
#         st=[]
#         for i in range(n):
#             if expression[i]==',':
#                 continue
#             elif expression[i] ==')':
#                 values=[]
#                 while st[-1]!='(':
#                     values.append(st.pop())
#                 st.pop()
#                 operator=st.pop()
#                 st.append(self.operatorValues(values,operator))
#             else:
#                 st.append(expression[i])
#         return  True if st[-1]=='t' else False
#             # return False
        

        
# a=Solution()
# print(a.parseBoolExpr("|(f,f,f,t)"))
# class Solution:
#     def maxUniqueSplit(self, s: str) -> int:

# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def kthLargestLevelSum(self, root, k):
        if not root:
            return []
        queue=[root]
        result=[]
        while queue:
            current_queue_size=len(queue)
            current_level=[]
            for i in range(current_queue_size):
                cuurent_node=queue.pop(0)
                current_level.append(cuurent_node.val)
                if cuurent_node.left:
                    queue.append(cuurent_node.left)
                if cuurent_node.right:
                    queue.append(cuurent_node.right)
            result.append(sum(current_level))
        result.sort(reverse=True)
        if len(result)>=k:
            return result[k-1]
        return -1
        
        
        

        