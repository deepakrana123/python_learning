from itertools import permutations
class Solution:
    # def smallestNumber(self,pattern):
    #     stack=[]
    #     j=1
    #     s=[]
    #     for i in range(len(pattern)+1):
    #         stack.append(j)
    #         j+=1
    #         if i==len(pattern) or pattern[i]=='I':
    #             while stack:
    #                 s.append(stack.pop())
    #     a=''
    #     for i in s:
    #         a+=str(i)
    #     return a
    
    def check(self,nums):
        
    def nextPermuation(self,nums):
        perms = sorted(set(permutations(nums)))
        for i, perm in enumerate(perms):
            if perm == tuple(nums) and i + 1 < len(perms):
                return list(perms[i + 1])
        return sorted(nums)

    def smallestNumber(self,pattern):
        nums=[i for i in range(1,len(pattern)+2)]
        print(nums,self.nextPermuation(nums))
        while self.check(nums)==False:
            nums=self.nextPermuation(nums)
        return [str(i) for i in nums]


a=Solution()
print(a.smallestNumber("IIIDIDDD"))
                


        