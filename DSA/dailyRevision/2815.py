def maxSum(nums):
    sums={}
    maxs=-1
    for i in range(len(nums)):
        a=max(list(str(nums[i])))
        if a in sums:
            maxs=max(maxs,sums[a]+nums[i])
        if a in sums:
            sums[a]=max(sums[a],nums[i])
        else:sums[a]=nums[i]
    return maxs
        
    
        

# def licenseKeyFormatting(s, k):
#     count=0
#     ans=''
#     i=len(s)-1
#     while i>=0:
#         if s[i]!='-':
#             ans+=s[i].upper()
#             count+=1
#         if count==k:
#             ans=ans +'_'
#             count=0
#         i-=1
#     s1=''
#     if len(ans)>0 and ans[-1]=='_':
#         ans=ans[0:len(ans)-1]
#     return ans[::-1]

# print(licenseKeyFormatting("2-5g-3-J", k = 2))
# print(licenseKeyFormatting("2-4A0r7-4k",4))
def compressedString(word):
    count=1
    prev=word[0]
    ans=''
    for i in range(1,len(word)):
        if word[i]==word[i-1]:
            if count==9:
                ans+=str(count)
        
    return ans

def countPrefixSuffixPairs(words):
    count=0
    def isPrefixSuffix(str1,str2):
        if len(str2)<len(str1):
            return False
        a=len(str1)
        if str1==str2[0:a] and str1==str2[::-1][0:a]:
            return True
        return False
        
    for i in range(len(words)):
        for j in range(i+1,len(words)):
            if isPrefixSuffix(words[i],words[j]):
                count+=1
    return count
                
# print(countPrefixSuffixPairs(["a","aba","ababa","aa"]))
def calculateScore(s):
    d={chr(i): chr(122 - (i - 97)) for i in range(97, 123)}
    sums=0
    asd={}
    for i in range(len(s)):
        reverseChar=d[s[i]]
        if reverseChar in asd and asd[reverseChar]:
            sums+=abs(i-asd[reverseChar].pop())
        else:
            if s[i] not in asd:
                asd[s[i]]=[]
            asd[s[i]].append(i)
    return sums
print(calculateScore("aczzx"))
print(calculateScore('abcdef'))
        

        

    

        