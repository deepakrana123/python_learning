def countBadPairs(nums):
    n=len(nums)
    dicts={}
    result=0
    for i in range(len(nums)):
        diff = nums[i]-i
        goodpairs = dicts.get(diff, 0)
        result+= (i-goodpairs)
        dicts[diff]=goodpairs+1
    return result


print(countBadPairs([1,2,3,4,5]))