import random
# class Solution:
#     def __init__(self, nums):
#         self.dicts={}
#         for i in range(len(nums)):
#             if nums[i] in self.dicts:
#                 self.dicts[nums[i]].append(i)
#             else:
#                 self.dicts[nums[i]]=[i]
#     def pick(self, target):
#         if target in self.dicts:
#             a = random.choice(self.dicts[target])
#             return a
#         return 0

# abc=Solution([1, 2, 3, 3, 3])
# abc.pick(3)
class Solution:
    def __init__(self, w):
        self.weight=w
        self.sums = sum(w)
        for i in range(len(self.weight)):
            self.weight[i]=self.weight[i]/self.sums
        for i in range(1,len(self.weight)):
            self.weight[i]+=self.weight[i-1]
    def pickIndex(self):
        N=random.uniform(0,1)
        flag=1
        index=-1
        while flag:
            index+=1
            if N<=self.weight[index]:
                flag=0
        return index
        

abc=Solution([1,3])
abc.pickIndex()
abc.pickIndex()
abc.pickIndex()
abc.pickIndex()
abc.pickIndex()

