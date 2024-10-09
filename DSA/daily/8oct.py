# class Solution:
#     def minSwaps(s):
#         a=[]
#         i=0
#         while i<len(s):
#             a.append(s[i])
#             if len(a) >= 2 and (a[-1]==']' and a[-2]=='['):
#                 a.pop()
#                 a.pop()
#             i+=1
#         count=0
#         print(a)
#         for si in a:
#             if si=='[':
#                 count+=1
#         return (count+1)//2
# a=Solution
# print(a.minSwaps( s="[]"))
# class Solution:
#     def minAddToMakeValid(self, s: str) -> int:
#         a=[]
#         i=0
#         while i<len(s):
#             a.append(s[i])
#             if len(a) >= 2 and (a[-1]==')' and a[-2]=='('):
#                 a.pop()
#                 a.pop() 
#             i+=1
#         return len(a)
#         print(a)
        
# a=Solution()
# print(a.minAddToMakeValid( "((("))
# class Solution:
#     def beautifulSubstrings(self, s: str, k: int) -> int:
#         a=[]
#         for i in range(len(s)):
#             vowels=0
#             constants=0
#             str1=s[i]
#             if s[i] in 'aeiou':
#                 vowels+=1
#             else:
#                 constants+=1
#             for j in range(i+1,len(s)):
#                 if s[j] in 'aeiou':
#                     vowels+=1
#                 else:
#                     constants+=1
#                 str1+=s[j]
#                 if vowels==constants and (vowels*constants)%k==0:
#                     a.append(str1)
#         return len(a)
        
# a=Solution()
# print(a.beautifulSubstrings("bcdf",1))    
# class Solution:
#     def solve(self,stringlength,str1):
#         if len(str1)==stringlength:
#             self.result.append(str1)
#             if len(self.result)>self.k:
#                 return  self.result[self.k-1]
#             return
#         for i in range(len(self.a)):
#             if str1 and str1[-1]==self.a[i]:
#                 continue
#             newStr=str1+self.a[i]
#             self.solve(stringlength,newStr)
#     def getHappyString(self, n, k):
#         self.a=['a','b','c']
#         self.result=[]
#         self.k=k
#         # for i in range(len(self.a)):
#         return self.solve(n,'')
#         print(self.result)
        
# a=Solution()
# print(a.getHappyString(3,9))
# class Solution:
#     def getHappyString(self, n, k):
#         self.a = ['a', 'b', 'c']
#         result=[]

#         def genrateSubtring(n,str1):
#             if len(str1)==n:
#                 result.append(str1)
#                 return
#             for char in self.a:
#                 if str1 and str1[-1]==char:
#                     continue
#                 newStr=str1+char
#                 genrateSubtring(n,newStr)
#         genrateSubtring(n,"")
#         return "" if len(result)<k else result[k-1]
        
# a = Solution()
# print(a.getHappyString(n=1, k=4))  

class Solution:
    def buddyStrings(self, s: str, goal: str) -> bool:
        s1=list(s)
        goal1=list(goal)
        if len(s1)!=len(goal1):
            return False
        for i in range(len(s1)):
            if s1[i]!=goal1[i]:
                s1[i] = goal1[i]
        print(s1,goal1)
        
        return ''.join(s1)!=s
a=Solution()
print(a.buddyStrings("ab","ab"))

        
        
        
        