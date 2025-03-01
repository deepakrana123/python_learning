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
    # j = 0
    # for i in range(len(nums)):
    #     if nums[i] != 0:
    #         nums[j] = nums[i]
    #         j += 1
    # while j < len(nums):
    #     nums[j] = 0
    #     j += 1
    # return nums


print(applyOperations([847, 847, 0, 0, 0, 399, 416, 416, 879, 879, 206, 206, 206, 272]))
print(applyOperations([0, 1]))
