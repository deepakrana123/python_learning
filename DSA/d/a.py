# class Solution:
#     def solve(self, candidates,target,result,temp,index):
#         if target == 0:
#             result.append(temp[:])
#             return
#         if index >=len(candidates):
#             return
#         if candidates[index]<=target:
#             temp.append(candidates[index])
#             self.solve(candidates, target-candidates[index], result, temp, index)
#             temp.pop()
#         self.solve(candidates, target, result, temp, index + 1)
    
#     def minimumNumbers(self, num, k):
#         a=[]
#         for i in range(k,num+1,10):
#             a.append(i)
#         result=[]
#         self.solve(a,num,result,[],0)
#         minLength=float("inf")
#         for i in range(len(result)):
#             minLength=min(minLength,result[i])
# a=Solution()
# print(a.minimumNumbers( 58,  9))

# class Solution:
#     def canAliceWin(self, nums):
#         nums.sort()  # Sort the numbers
#         index=0
#         for i in range(len(nums)):
#             if len(str(nums[i]))!=1:
#                 index=i
#                 break
#         sums = sum(nums[:index])
#         sums1 = sum(nums[index:])
#         if sums==sums1:
#             return False
#         return True
#         print(sums,sums1)
        
# a=Solution()
# print(a.canAliceWin([1,2,3,4,10]))
# class Solution:
#     def sumOfThree(num):
#         if num%3!=0:
#             return []
#         return [num//3-1,num//3,num//3+1]
class Solution:
    def longestContinuousSubstring(self,s):
        l=0
        compareStr="abcdefghijklmnopqrstuvwxyz"
        maxLength=1
        n=len(s)
        i=0
        while l<n:
            if s[l]==compareStr[i]:
                i+=1
            elif s[l]!=compareStr[i]:
                i=0
            l+=1
            maxLength=max(maxLength,i)
        return maxLength
a=Solution()
print(a.longestContinuousSubstring("abacaba"))
        
            
        
        