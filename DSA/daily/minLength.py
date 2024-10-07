# class Solution:
#     def minLength(self, s):
#         a=[]
#         i=0
#         while i<len(s):
#             print(a)
#             if len(a) >= 2 and ((a[-1]=='B' and a[-2]=='A') or (a[-1]=='D' and a[-2]=='C')):
#                 print(a,"a")
#                 a.pop()
#                 a.pop()
#             a.append(s[i])
#             i+=1
#         return len(a)
# a=Solution()
# print(a.minLength("DKCABD"))
# class Solution:
#     def addedInteger(self, nums1, nums2):
#         nums2.sort()
#         min1=min(nums2)
#         min2=min(nums1)
#         sub=min1-min2
#         nums1.sort()
#         # for i in range(len(nums1)):
#         #     nums1[i]=nums1[i]+sub
#         # print(nums1)
#         return sub
# a=Solution()
# print(a.addedInteger([10], nums2 = [5]))
from collections import Counter
class Solution:
    def reportSpam(self, message, bannedWords):
        count=Counter(bannedWords)
        booleanTrue=0
        for word in message:
            if word in count:
                booleanTrue+=1
            if booleanTrue>=2:
                return True
        return False
        
a=Solution()
print(a.reportSpam( ["l","i","l","i","l"], ["d","a","i","v","a"]))
        
        


        
        