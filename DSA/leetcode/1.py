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
    def check_vowel_order(self,char1, char2):
        vowels = "aeiou"
        index1 = vowels.find(char1)
        index2 = vowels.find(char2)
        if index1 != -1 and index2 == index1 + 1:
            return True
        else:
            return False
    def longestBeautifulSubstring(self,word: str) -> int:
        if len(word)<5:
            return 0
        l=0
        r=0
        for i in range(len(word)):
            if word[i]=='a':
                l=i
                r=i
                break
        prev=r
        r=r+1
        maxLength=0
        while r<len(word):
            if self.check_vowel_order(word[prev],word[r]):
                maxLength=max(maxLength,r-l+1)
            while self.check_vowel_order(word[prev],word[r])==False:
                prev=l
                l+=1
            prev=r
            r+=1
                
        return maxLength
        
        print(l,r)

a=Solution
print(a.longestBeautifulSubstring("aeiaaioaaaaeiiiiouuuooaauuaeiu"))