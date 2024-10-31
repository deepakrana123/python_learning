def convertBinary(n):
    abc=[]
    i=0
    while n>0:
        rem=n%2
        abc.append(rem)
        n=n//2
    a=0
    for i in range(len(abc)):
        a+=abc[i]*pow(2,i)
    abc.reverse()
    return (abc,a)
# print(convertBinary(14))
# class Solution:
#     def addContirbution(self,val,bitArray,flag):
#         i=0
#         while val>0:
#             bitArray[i]=bitArray[i]+(1 if flag else -1)*(val%2)
#             val//=2
#             i+=1
#     def isContribution(self,k,biArray):
#         bitVectorValue=0
#         for i in range(32):
#             bitVectorValue+=(1 if biArray[i]>0 else 0)*pow(2,i)
#         return bitVectorValue>=k
#     def minimumSubarrayLength(self,nums, k):
#         i=0
#         j=0
#         ordValue=[0]*32
#         ans=float("inf")
#         while j<len(nums):
#             self.addContirbution(nums[j],ordValue,True)
#             while self.isContribution(k,ordValue) and i<j:
#                 ans=min(ans,j-i+1)
#                 self.addContirbution(nums[i],ordValue,False)
#                 i+=1
#             j+=1
#         return ans if ans!=float("inf") else -1
            
# a=Solution()
# print(a.minimumSubarrayLength([1,12,2,5], k = 43))
# def maximumOddBinaryNumber(s: str):
#         b=sum([1 for num in s if num=='1'])
#         if b==0:
#             return s
#         b=b-1
#         return "1" * b + "0" * (len(s) - b - 1) + "1"
# print(maximumOddBinaryNumber("1010"))
from collections import Counter
class Solution:
    def wonderfulSubstrings(self,word):
        a=[]
        for i in range(len(word)):
            for j in range(i,len(word)):
                a.append(word[i:j+1])
        count=0
        for i in range(len(a)):
            dicts=Counter(a[i])
            countOdd=0
            for key in dicts:
                if dicts[key]%2!=0:
                    countOdd+=1
            if countOdd<=1 :
                count+=1
        return count
a=Solution()
print(a.wonderfulSubstrings("he"))
        