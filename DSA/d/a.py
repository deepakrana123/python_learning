def check_numbers(nested_list):
    for i in range(len(nested_list)):
        if i % 2 == 0:
            for j in range(1, len(nested_list[i])):
                if nested_list[i][j] % 2 != 0 or nested_list[i][j-1] >= nested_list[i][j]:
                    return False
        else:
            for j in range(1, len(nested_list[i])):
                if nested_list[i][j] % 2 == 0 or nested_list[i][j-1]>= nested_list[i][j]:
                    return False
    return True


# Example usage:
nested_list = [[2], [12, 8], [5, 9], [18, 16]]
nested_list1 = [[1], [10, 4], [3, 7, 9], [12, 8, 6, 2]]
result = check_numbers(nested_list)
print(result)  # Should return True or False
# class Solution:
#     def kthSmallestProduct(self, nums1: List[int], nums2: List[int], k: int) -> int:
from collections import Counter
class Solution:
    def largestPalindromic(self, num: str) -> str:
        count=Counter(num)
        if all(x=="0" for x in num):
            return "0"
        list1=list(count.keys())
        flag=0
        maxE=0
        for value in list1:
            if count[value]%2!=0: 
                flag=1
                maxE=max(maxE,int(value))
                count[value]-=1
                if count[value]==0:
                    del count[value]
        t=""
        if flag:
            t+=str(maxE)
        list2=list(count.keys())
        list2.sort()
        if list2==[] or list2==[""]:
            return t
        for value in list2:
            t=value*(count[value]//2)+t
            t+=value*(count[value]//2)
        return t
a=Solution()

class Solution:
    def solve(self, currnum,originalnum,result):
        if currnum>originalnum:
            return
        # result.append(currnum)
        result[0]+=1
        for i in range(10):
            number_set = set(str(currnum))
            if str(i) in number_set:
                continue
            a=currnum*10+i
            if a > originalnum:
                return
            self.solve(a,originalnum,result)
        return result
    def countSpecialNumbers(self, n: int,) -> int:
        result=[0]  
        for i in range(1,10):
            self.solve(i,n,result)
        return result[0]
a=Solution()
# print(a.countSpecialNumbers(5))
import math
class Solutions:
    def trailingZeroes(self,n):
        count=0
        c=math.factorial(n)
        while c>0:
            if c%10==0:
                count+=1
                c=c//10
            else:
                return count
        return count
b=Solutions()
print(b.trailingZeroes(120))
        