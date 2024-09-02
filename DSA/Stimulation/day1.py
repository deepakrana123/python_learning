import random
class Solution:
    def __init__(self, nums):
        self.nums=nums
        self.obj=nums.copy()
    def reset(self):
        return self.obj

    def shuffle(self):
        r=[i for i in range(len(self.nums))]
        random.shuffle(r)
        self.nums=[self.nums[i] for i in r]
        return self.nums 
obj=Solution([1, 2, 3])
print(obj.reset())
print(obj.shuffle())

class Solution1:
    def grayCode(self,n):
        print(n,n|1)

obj1=Solution1()
print(obj1.grayCode(2))