def maximumSumSubarray(num,k):
    i=0
    j=0
    # first build the window size
    # do basic calculation till window size
    # do calculation when window size get hits and mantain the window size
    max1=float("-inf")
    maxSum=float("-inf")
    sum1=0
    while(i<j and j<len(num)):
        sum1+=num[j]
        if(j-i+1<k):
            j+=1
        if(j-i+1==k):
            if maxSum<sum1:
                max1=max(max1,j-i+1)
                maxSum=max(sum1,maxSum)
                sum1-=num[i]
                i+=1
                j+=1
        
def firstNegativeValue(num,k):
    i=0
    j=0
    arr=[]
    result=[]
    if len(num)==0:
        return 0
    while(j<len(num)):
        if arr[j]<0:
            arr.append(num[j])
        if j-i+1<k:
            j+=1
        if j-i+1==k:
            if len(arr)==0:
                return 0
            else:
                result.append(arr[0])
                arr.pop(0)
                i+=1
                j+=1

# def removeZeroSumSublists(self, head):
#         dict1={}
#         dummy.value=0
#         dummy.next=head
#         prefixSum=0
#         while(head and head.next!=None):
#             prefixSum+=head.value
#             if dict1.get(prefixSum):
#                 start=dict1[prefixSum]
#                 temp=start
#                 while(temp!=head):
#                     temp=temp.next
#                     prefixSum=temp.value
#                     if temp!=head:
#                         del dict[prefixSum]
#                 start.next=head.next
#             else:
#                 dict1[prefixSum]=head
#             head=head.next
#         return dummy.next
                    
def longestSubstringWithKUniqueCharacters(arr,k):
    i=0
    j=0
    n=len(arr)
    dict1={}
    ans=float("-inf")
    while(j<n):
        if dict1.get(arr[j]):
            dict1[arr[j]]+=1
        else:
            dict1[arr[j]]=1
        if len(dict1)<k:
            j+=1
        elif len(dict1)==k:
            ans=max(ans,j-i+1)
            j+=1
        elif len(dict1)>k:
            while(len(dict1)>k):
                if(dict1[arr[i]]!=0):
                    dict1[arr[i]]-=1
                else:
                    del dict1[arr[i]]
                i+=1
    return ans
def numSubarraysWithSum(nums, goal):
    i=0
    j=0
    n=len(nums)
    ans=0
    sum1=0
    while(j<n and i<n):
        sum1+=nums[j]
        if sum1<goal:
            j+=1
        elif sum1==goal:
            ans+=1
            j+=1
        elif sum1>goal:
            while(sum1>goal):
                # print(i)
                print(sum1,i,j,nums[i],"m")
                sum1=sum1-nums[i]
                i+=1
            j+=1
    return ans
# print(numSubarraysWithSum([1,0,1,0,1],2))
from collections import deque 
# def numberOfSubarrays(nums, k):
#     de=deque([])
#     i=0
#     j=0
#     count=0
#     ans=0
#     while(j<len(nums)):
#         # print(nums[j],i)
#         if nums[j]%2!=0:
#             count+=1
#             de.append(nums[j])
#         else:
#             de.append(nums[j])
#         if count < k:
#             j += 1
#         elif count == k:
#             ans += 1
#             while(count==k):
#                 ans+=1
#                 a=de.popleft()
#                 if a%2!=0:
#                     count-=1
#                 else:
#                     break
#                 i+=1
#             j+=1
#         elif count>k:
#             while(count>k):
#                 a=de.popleft()
#                 if a%2!=0:
#                     count-=1
#                 else:
#                     break
#                 i+=1
#             j+=1
#     return ans
from collections import deque 

def numberOfSubarrays(nums, k):
    de = deque([])
    i = 0
    j = 0
    count = 0
    ans = 0
    
    while j < len(nums):
        if nums[j] % 2 != 0:
            count += 1
        de.append(nums[j])
        if count < k:
            j += 1
        elif count == k:
            ans += 1
            while count == k and de and de[0]%2==0:
                de.popleft()
                i += 1
            j += 1
        elif count > k:
            while count > k:
                a = de.popleft()
                if a % 2 != 0:
                    count -= 1
                else:
                    break
                i += 1
            j += 1
    
    return ans

print(numberOfSubarrays([2,2,2,1,2,2,1,2,2,2], 2))

print(numberOfSubarrays([2,2,2,1,2,2,1,2,2,2],2))
        
        
            

        
            
            
                  