# class Solution:
#     def canArrange(self, arr, k):
#         if len(arr)%2!=0:
#             return False
#         # num=[((num % k)+k)%k for num in arr ]
#         # print(num)
#         # count=Counter(num)
#         # if count[0]%2!=0:
#         #     return False
#         # for i in range(1,k//2):
#         #     countHalf= k-i
#         #     if count[countHalf]!=count[i]:
#         #         return False
#         # return True
#         dicts={}
#         for i in range(len(arr)):
#             arr[i]=((arr[i]%k)+k)%k
#             if arr[i] in dicts:
#                 dicts[arr[i]]+=1
#             else:
#                 dicts[arr[i]]=1
#         print(dicts,arr)
#         if 0 in dicts and dicts[0]%2!=0:
#             return False
#         for i in range(1,k//2+1):
#             print(i,k)
#             currHalf=k-i
#             if dicts[currHalf]!=dicts[i]:
#                 return False
#         return True
# a=Solution()
# print(a.canArrange([-1,-1,-1,-1,2,2,-2,-2],3))
# class Solutions:
#     def computeGCD(self,x, y):
#         while(y):
#             x, y = y, x % y
#         return abs(x)
#     def countPairs(self, arr, k):
#         dicts={}
#         nums=[0]*len(arr)
#         for i in range(len(arr)):
#             arr_gcd=k//self.computeGCD(arr[i],k)
#             dicts[arr_gcd]=dicts.get(arr_gcd,0)+1
#         print(dicts,arr,nums)
# a=Solutions()
# print(a.countPairs([1,2,3,4,5], k = 2))
class Solution:
    def arrayRankTransform(self, arr):
        a=sorted(arr)
        abc=[0]*len(a)
        dicts={}
        count=1
        for i in range(len(a)):
            if a[i] in dicts:
                continue
            dicts[a[i]]=count
            count+=1
        for i in range(len(arr)):
            abc[i]=dicts[arr[i]]
        return abc


a=Solution()
print(a.arrayRankTransform([40,10,20,30]))
        
        

        



        
            
        