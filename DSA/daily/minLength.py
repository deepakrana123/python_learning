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
# from collections import Counter
# class Solution:
#     def reportSpam(self, message, bannedWords):
#         count=Counter(bannedWords)
#         booleanTrue=0
#         for word in message:
#             if word in count:
#                 booleanTrue+=1
#             if booleanTrue>=2:
#                 return True
#         return False
        
# a=Solution()
# print(a.reportSpam( ["l","i","l","i","l"], ["d","a","i","v","a"]))
# class Solution:
#     def minimumAddedInteger(self, nums1, nums2):
#         nums1.sort()
#         nums2.sort()
#         mins1,maxs1=min(nums1),max(nums1)
#         mins2,maxs2=min(nums2),max(nums2)
#         m=maxs2-maxs1
#         n=mins2-mins1
#         return m if n>m else m
# a=Solution()
# print(a.minimumAddedInteger([3,5,5,3], nums2 = [7,7]))
# var twoSum=function(nums,target,start,end){
#   let r=[]
#     while(start<end){
#         if(nums[start]+nums[end]>target){
#             end--
#         }
#         else if(nums[start]+nums[end]<target){
#             start++
#         }
#         else{
#             while(nums[start]===nums[start+1] && start<end) start++;
#             while(nums[end]===nums[end-1] && start<end) end--
#             r.push([-target,nums[start],nums[end]])
#             start++;
#             end--;
#         }
#     }
#    return r
   
# # }
# class Solution:
#     def two_sum(self,nums,target,start,end):
#         # num_map = {}
#         # for i, num in enumerate(nums):
#         #     complement = target - num
#         #     if complement in num_map:
#         #         return [num_map[complement], i]
#         #     num_map[num] = i
#         # return []
#         num_map=[]
#         while start<end:
#             if nums[start]+nums[end]>target:
#                 end-=1
#             elif nums[start]+nums[end]<target:
#                 start+=1
#             else:
#                 while nums[start]==nums[start+1] and start<end:
#                      start+=1
#                 while nums[end]==nums[end-1] and start<end:
#                     end-=1
#                 num_map.append([-target,nums[start],nums[end]])
#                 start+=1
#                 end-=1
#         return num_map

#     def threeSum(self,nums):
#         nums.sort()
#         a=[]
#         if len(nums)<3:
#             return []
#         for i in range(len(nums)):
#             if i>0 and nums[i]==nums[i-1]:
#                 continue
#             target=-nums[i]
#             a.append(self.two_sum(nums,target,i+1,len(nums)-1))
#         flattened_arr = [item for sublist in a if sublist for item in sublist]
#         return flattened_arr
            
#     def twoSum2(self,nums,n1,n2,target):
#         print(nums,n1,n2,target)
#         newTarget=target-nums[n1]-nums[n2]
#         num_map = {}
#         for i, num in enumerate(nums):
#             complement = newTarget - num
#             if i!=n1 and i !=n2 and complement in num_map:
#                 return [complement,nums[i],nums[n1],nums[n2] ]
#             num_map[num] = i
#         return []

#     def fourSum(self, nums, target):
#         nums.sort()
#         a=[]
#         if len(nums)<4:
#             return []
#         for i in range(1,len(nums)):
#             a.append(self.twoSum2(nums,i-1,i,target))
#         return a
# a=Solution()
# print(a.fourSum([1,0,-1,0,-2,2], target = 0))
        
        
# class Solution:
#     def reorganizeString(self, s: str) -> str:
#         dicts={}
# from heapq import heapify, heappush, heappop 
# class Solution:
#     def kthSmallestPrimeFraction(self, arr, k):
#         heap = [] 
#         heapify(heap)
#         for i in range(len(arr)):
#             for j in range(i+1,len(arr)):
#                 heappush(heap,(arr[i]/arr[j],[arr[i],arr[j]]))
#         a=0
#         while k>0:
#             a=heappop(heap)
#             k-=1
#         return a[1]
# a=Solution()
# print(a.kthSmallestPrimeFraction([1,7], k = 1))
# class Solution:
#     def solve(self, candidates,target,result,temp,index):
#         if target == 0:
#             result.append(temp[:])
#             return
#         if index >=len(candidates):
#             return
#         if candidates[index]<=target:
#             temp.append(candidates[index])
#             self.solve(candidates, target-candidates[index], result, temp, index)
#             temp.pop()
#         self.solve(candidates, target, result, temp, index + 1)
#     def minimumNumbers(self, num: int, k: int) -> int:
#         a=[]
#         for i in range(k,num+1,10):
#             a.append(i)
#         if num==0 and k==0:
#             return 0
#         if num <10 and k==0:
#             return -1
#         if num==10 and k==0:
#             return 1
#         result=[]
#         print(a)
#         self.solve(a,num,result,[],0)
#         minLength=float("inf")
#         for i in range(len(result)):
#             minLength=min(minLength,len(result[i]))
#         return -1 if minLength==float("inf") else minLength
# a=Solution()
# print(a.minimumNumbers(10,0))
# class Solution:
#     def findLonely(self,nums):
#         h={}
#         a=[]
#         for num in nums:
#             if num not in h:
#                 h[num] = 1
#             else:
#                 h[num] += 1  
#         for num in nums:
#             if num-1 in h:
#                 continue
#             if num+1 in h:
#                 continue
#             if num in h and h[num]==1:
#                 a.append(num)
#         return a
#         print(a)
        
# a=Solution()
# print(a.findLonely([1,3,5,3]))
class Solution:
    def maxFrequency(self, nums, k):
        nums.sort()
        i=0
        j=0
        n=len(nums)
        sums=0
        ans=1
        while j<n:
            sums+=nums[j]
            while j<n and (j-i+1)*nums[j]-sums>k:
                sums-=nums[i]
                i+=1
            ans=max(j-i+1,ans)
            j+=1
        return ans
a=Solution()
print(a.maxFrequency([3,9,6], k = 2))

        


        
        

        


        