
def longestSubarray(nums):
        i = 0
        j = 0
        n = len(nums)
        count = 0
        ans = 0
        while j <n:
            if nums[j]==0:
                count+=1
                

            while count > 1:
                print(j,i)
                ans = max(ans, j-i)
                count -= 1 if nums[i] == 0 else 0
                i += 1
            j += 1
        return ans
    
print(longestSubarray([1,1,0,1]))
        