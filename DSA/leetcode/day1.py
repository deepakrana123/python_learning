def lengthOfLastWord(s):
    x=s.split(" ")
    for i in range(len(x)-1,-1,-1):
        if x[i]!="":
            return x[i]
    # a=s.strip()
    # j=0
    # for i in range(len(a)-1,-1,-1):
    #     if a[i]==" ":
    #         j=i
    #         break
    # return len(a[j+1:len(a)])
def maxSubarrayLength(nums, k):
    i=0
    j=0
    h={}
    result=0
    while j<len(nums):
        if nums[j] in h:
            h[nums[j]]+=1
        else:
            h[nums[j]]=1
        while i<j and h[nums[j]]>k:
            h[nums[i]]-=1
            i+=1
        print(i,j,h)
        result=max(j-i+1,result)
        j+=1
    return result

def checkIfValueIncreaseFormThere(dicts,k):
    for key in dicts:
        if dicts[key]==k: 
            return True
    return False

# def firstMissingPositive(nums):
#     if 1 not in nums:
#         return 1
    
def isIsomorphic(s, t):
    dict1={}
    dict2={}
    a=""
    b=""
    for key in range(len(s)):
        if s[key] in dict1 and dict1[s[key]]!= t[key] or t[key] in dict2 and dict2[t[key]]!=s[key]:
            return False
        else:
            dict1[s[key]]=t[key]
            dict2[t[key]]=s[key] 
    return len(dict1)==len(dict2)
def numSubarrayProductLessThanK(nums, k):
    count=0
    i=0
    j=0
    mul=1
    if k==0:
        return 0
    while j<len(nums):
        mul+=nums[j]
        while mul//k==0:
                mul=mul-nums[i]
                i+=1
        count+=j-i+1
        j+=1
    return count
print(numSubarrayProductLessThanK([4,5,0,-2,-3,1],9))        
def findWordsContaining(words, x):
        a=[]
        for i in range(len(words)):
            if x in words[i]:
                a.append(i)
        return a
print(findWordsContaining(["abc","bcd","aaaa","cbc"],"a"))
# def maxVowels(s, k):
#     dict1={"a":0,"e":0,"i":0,"o":0,"u":0}
#     i=0
#     j=0
#     m=""
#     while j<len(s):
#         m+=s[j]
#         if len(m)<k:
#             if 
            
      
#  def subarraysDivByK(nums, k) -> int:
     count=0
     i=0
     j=0
     count+=1 if k==sum(nums) else 0
    #  while j<len(nums):
          
        