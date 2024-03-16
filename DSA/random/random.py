def productExceptSelf(nums):
    left=[1]
    right=[0]*(len(nums))
    right[len(nums)-1]=1
    for i in range(1,len(nums)):
        left.append(nums[i-1]*left[i-1])
    for i in range(len(nums)-2,-1,-1):
        right[i]=nums[i+1]*right[i+1]
    result=[0]*len(nums)
    for i in range(len(nums)):
        result[i]=left[i]*right[i]
    return result
        
print(productExceptSelf([1,2,3,4]))

def subarraySum(nums,k):
    left=[0]*len(nums)
    left[0]=nums[0]
    for i in range(1,len(nums)):
        left[i]=nums[i]+left[i-1]
    dict1={}
    dict1[0]=1
    result=0
    for i in range(len(left)):
        val=left[i]-k
        if val in dict1:
            result+=dict1[val]
            dict1[val]+=1
        else:
            dict1[left[i]]=1
    return result
print(subarraySum([1,-1,0],0))