# class Solution:
#     def stringHash(self, s: str, k: int) -> str:
#         if len(s) % k != 0:
#             return ""
#         parts = [s[i:i + k] for i in range(0, len(s), k)]
#         a = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h', 8: 'i', 9: 'j', 10: 'k', 11: 'l', 12: 'm',
#              13: 'n', 14: 'o', 15: 'p', 16: 'q', 17: 'r', 18: 's', 19: 't', 20: 'u', 21: 'v', 22: 'w', 23: 'x', 24: 'y', 25: 'z'}
#         result=""
#         for i in range(len(parts)):
#             s=0
#             for j in range(len(parts[i])):
#                 s+=ord(parts[i][j])-ord('a')
#             s%=26
#             result+=a[s]
#         return result


# a = Solution()
# print(a.stringHash("abcd", k=2))
# class Solution:
#     def minIncrementForUnique(self, nums):
#         nums.sort()
#         count=0
#         s=set()
#         s.add(nums[0])
#         for i in range(1,len(nums)):
#             if nums[i] in s:
#                 count+=nums[i-1]+1-nums[i]
#                 nums[i]=nums[i-1]+1
#                 s.add(nums[i])
#             else:
#                 s.add(nums[i])
#         return count
# a=Solution()
# print(a.minIncrementForUnique([1,2,2]))
# class Solution:
#     def missingRolls(self, rolls, mean: int, n: int):
#         sums=sum(rolls)
#         s=n+len(rolls)
#         target_sum=s*mean-sums
#         x=target_sum//n
#         y=target_sum%n
#         a=[]
#         if x<=0 or x>6:return a
#         if x==6 and y>0:return a
#         for i in range(n):
#             a.append(x)
#         for i in range(y):
#             a[i]=a[i]+1


#         return a
# a=Solution()
# print(a.missingRolls([1,2,3,4], mean = 6, n = 4))
# Definition for singly-linked list.
class Solution:
    def minimumCost(self, cost):
        cost.sort()
        costs=0
        if len(cost)%3!=0:
            return costs
        for i in range(len(cost)-1,-1,-1):
            if i%3==0 or i==0:
                continue
            costs+=cost[i]
        return costs
a=Solution()
print(a.minimumCost([1,2,3]))
        
        
        
