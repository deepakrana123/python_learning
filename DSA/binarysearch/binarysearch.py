def binarySearch(arr,element):
    left=0
    right=len(arr)-1
    while left<=right:
        mid=(right-left)//2 + left
        if arr[mid]==element:
            return mid
        elif arr[mid]<element:
            left=mid+1
        else:
            right=mid-1
    return mid

def searchInsertPosition(arr,element):
    left = 0
    right = len(arr)-1
    while left <=right:
        mid=(right+left)//2
        if arr[mid] == element:
            return mid
        elif arr[mid]<element:
            left=mid+1
        else:
            right=mid-1
    return right + 1

# def firstBadVersion(n):
#     low=0
#     high=n
#     while low<=high:
#         mid=(high-low)//2+low
#         if isBadVersion(mid):
#             high=mid
#         else:
#             low=mid+1
# class Solution:
#     def SieveOfEratosthenes(self):
#         self.prime[0] = self.prime[1] = False
#         p = 2
#         while (p * p <= 1000):
#             if self.prime[p]:
#                 for i in range(p * p, 1001, p):
#                     self.prime[i] = False
#             p += 1 
#     def primeSubOperation(self, nums):
#         self.prime = [True for i in range(1001)]
#         self.SieveOfEratosthenes()
#         for i in range(len(nums)-2,-1,-1):
#             if nums[i]<nums[i+1]:
#                 continue
#             else:
#                 for p in range(2,nums[i]):
#                     if self.prime[p] is False:
#                         continue
#                     if self.prime[p] and nums[i]-p<nums[i+1]:
#                         nums[i]-=p
#                         break
#             if nums[i]>=nums[i+1]:
#                 return False
#         return True


# a=Solution()
# print(a.primeSubOperation([4,9,6,10]))

# class Solution:
#     def binarySearch(self,arr,element):
#         left = 0
#         right = len(arr)-1
#         ans=0
#         mid=0
#         while left <= right:
#             mid = (right-left)//2 + left
#             if arr[mid][0] >element:
#                 right = mid - 1
#             else:
#                 ans=max(ans,arr[mid][1])
#                 left = mid + 1
#         return ans
#     def maximumBeauty(self, items, queries):
#         extra_items = sorted(items, key=lambda index : index[0])
#         for i in range(1,len(extra_items)):
#             if extra_items[i][1]<extra_items[i-1][1]:
#                 extra_items[i][1]=extra_items[i-1][1]
#         result=[]
#         for query in queries:
#             result.append(self.binarySearch(extra_items,query))
#         return result


        
            
# a=Solution()
# print(a.maximumBeauty( [[1,2],[3,2],[2,4],[5,6],[3,5]],[1,2,3,4,5,6]))

# class Solution:
#     def lowerBound(self,nums,target):
#         start=0
#         end=len(nums)-1
#         ans=-1
#         while start<=end:
#             mid=(end-start)//2+start
#             if nums[mid]>=target:
#                 ans=mid
#                 end=mid-1
#             else:
#                 start=mid+1
#         return ans
#     def upperBound(self,nums,target):
#         start=0
#         end=len(nums)-1
#         ans=-1
#         while start<=end:
#             mid=(end-start)//2+start
#             if nums[mid]>target:
#                 ans=mid
#                 end=mid-1
#             else:
#                 start=mid+1
#         return ans

#     def countFairPairs(self, nums, lower, upper):
#         nums.sort()
#         count=0
#         for i in range(len(nums)):
#             print(self.lowerBound(nums[i+1:],lower-nums[i]),self.upperBound(nums[i+1:],upper-nums[i]))
#             count+=(self.upperBound(nums[i+1:],upper-nums[i])-1-i)-(self.lowerBound(nums[i+1:],lower-nums[i])-1-i)
#         return count
# a=Solution()
# print(a.countFairPairs([1,7,9,2,5], lower = 11, upper = 11))
        


class SOlution:
    def singleElementInSortedArray(self,arr):
        p=arr[0]
        count=1
        ans=-1
        for i in range(1,len(arr)):
            if p!=arr[i] and count==1:
                ans=p
            if p==arr[i]:
                count+=1
            elif p!=arr[i]:
                
                p=arr[i]
                count=1
        return ans if ans!=-1 else p if count==1 else -1
a=SOlution()
print(a.singleElementInSortedArray( [1, 1, 2, 2, 3,3,5, 4, 4, 7, 7,8,8]))
        


