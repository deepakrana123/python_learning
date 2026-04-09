def applyOperations(nums):
    j = 0
    for i in range(len(nums)):
        if i + 1 < len(nums) and nums[i] == nums[i + 1] and nums[i] != 0:
            nums[i] = nums[i] * 2
            nums[i + 1] = 0
        if nums[i] != 0:
            if i != j:
                temp = nums[i]
                nums[i] = nums[j]
                nums[j] = temp
            j += 1
    return nums


def mergeArrays(nums1, nums2):
    dicts = {}
    for u, v in nums1 + nums2:

        if u in dicts:
            dicts[u] = dicts.get(u) + v
        else:
            dicts[u] = v
    sorted_dicts = dict(sorted(dicts.items()))
    a = []
    for key in sorted_dicts:
        a.append([key, sorted_dicts[key]])
    return a


print(mergeArrays([[1, 2], [2, 3], [4, 5]], nums2=[[1, 4], [3, 2], [4, 1]]))
