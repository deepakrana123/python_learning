def wordSubsets(words1, words2):
    def isSubSet(freq,temp):
        for i in range(26):
            if temp[i]<freq[i]:
                return False
        return True
    freq=[0]*26
    for word in words2:
        temp=[0]*26
        for w in word:
            temp[ord(w)-ord('a')]+=1
            freq[ord(w)-ord('a')]=max(freq[ord(w)-ord('a')],temp[ord(w)-ord('a')])
    result=[]
    for word in words1:
        temp=[0]*26
        for ch in word:
            temp[ord(ch)-ord('a')]+=1
        if isSubSet(freq,temp):
            result.append(word) 
    return result       
def canConstruct(s, k):
    dicts={}
    if len(s)==k:
        return True
    if len(s)<k:
        return False
    for ch in s:
        dicts[ch]=dicts.get(ch,0)+1
    countOddChar=0
    for ch in dicts:
        if dicts[ch]%2!=0:
            countOddChar+=1
    return countOddChar<=k
# print(canConstruct("true", k = 4))
print(wordSubsets(["amazon","apple","facebook","google","leetcode"], words2 = ["e","o"]))
print(wordSubsets(["amazon","apple","facebook","google","leetcode"], words2 = ["lc","eo"]))