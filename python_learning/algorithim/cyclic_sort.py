#  it usually used when you need a way to sort or find missing in 1 to n in array


# tc=o(n) and space o(1) ,
def cylic_sort(nums):
    i = 0
    n = len(nums)
    while i < len(nums):
        correct_index = nums[i] - 1
        if nums[i] < n and nums[i] != nums[correct_index]:
            nums[i], nums[correct_index] = nums[correct_index], nums[i]
        else:
            i += 1
    return nums


def cyclic_sorted_noted(nums):
    for i in range(len(nums)):
        if nums[i] < 0:
            nums[i] = 0
    i = 0
    n = len(nums)
    while i < len(nums):
        correct_index = nums[i]
        if nums[i] < n and nums[i] != nums[correct_index]:
            nums[i], nums[correct_index] = nums[correct_index], nums[i]
        else:
            i += 1
    return nums


print(cyclic_sorted_noted([-3, -2, -1, 1, 5, 4, 2]))
