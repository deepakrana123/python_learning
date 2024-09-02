# class Solution:
#     def count2Frequency(self,dicts):
#         for key,value in dicts.items():
#             if dicts[key]==2:
#                 return True
#         return False
        
#     def lengthOfLongestSubstring(self, s: str) -> int:
#         i=0
#         j=0
#         ans=float("-inf")
#         n=len(s)
#         dicts={}
#         while j<n:
#             dicts[s[j]]=dicts.get(s[j],0)+1
#             if self.count2Frequency(dicts):
#                 while self.count2Frequency(dicts):
#                     dicts[s[i]]-=1
#                     if dicts[s[i]]==0:
#                         del dicts[s[i]]
#                     i+=1
#             ans=max(ans,j-i+1)
#             j+=1
#         return ans
# a=Solution()
# print(a.lengthOfLongestSubstring("abcabcbb"))
# class Solution:
#     def count2Frequency(self,dicts):
#         for key,value in dicts.items():
#             if dicts[key]==2:
#                 return True
#         return False
        
#     def maximumUniqueSubarray(self, s) -> int:
#         if len(s)==0:
#             return 0
#         ans=float("-inf")
#         i=0
#         j=0
#         n=len(s)
#         dicts={}
#         sums=0
#         while j<n:
#             if s[j] in dicts:
#                 while s[j] in dicts:
#                     sums -= s[i]
#                     dicts[s[i]] -= 1
#                     if dicts[s[i]] == 0:
#                         del dicts[s[i]]
#                     i += 1
#             dicts[s[j]]=dicts.get(s[j],0)+1
#             sums+=s[j]
#             ans=max(ans,sums)
#             j+=1
#         return ans
# a=Solution()
# print(a.maximumUniqueSubarray([4,2,4,5,6]))
 
class Solution:
    def characterReplacement(self, s: str, k: int) -> int:
        i=0
        j=0
        dicts={}
        maxLength=float("-inf")
        n=len(s)
        while j<n:
            dicts[s[j]]=dicts.get(s[j],0)+1
            if len(dicts)<=k:
                maxLength=max(maxLength,j-i+1)
            if len(dicts)>k:
                while len(dicts)>k:
                    dicts[s[i]]-=1
                    if dicts[s[i]]==0:
                        del dicts[s[i]]
                    i+=1
            j+=1
        return maxLength
a=Solution()
print(a.characterReplacement("AABABBA", 1))