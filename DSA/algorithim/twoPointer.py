# Two Pointers = using two indices (often left and right) to iterate through a sequence (like an array or string) more efficiently than nested loops.


def twopointer(nums):
    i = 0
    j = 1
    while j < len(nums):
        if nums[j] != nums[i]:
            i += 1
            nums[j], nums[i] = nums[i], nums[j]
        j += 1
    return nums


def dutchFalgProblem(nums):
    low = 0
    mid = 0
    high = len(nums) - 1
    while mid <= high:
        if nums[mid] == 2:
            nums[mid], nums[high] = nums[high], nums[mid]
            high -= 1
        elif nums[mid] == 0:
            nums[mid], nums[low] = nums[low], nums[mid]
            low += 1
            mid += 1
        else:
            mid += 1
    return nums


def reverseString(s):
    strs = [i for i in s]
    start = 0
    end = len(strs) - 1
    while start <= end:
        strs[start], strs[end] = strs[end], strs[start]
        end -= 1
        start += 1
    return "".join(strs)


def validPalindrome(s):
    strs = [i for i in s]
    start = 0
    end = len(strs) - 1
    while start <= end:
        if strs[end] == strs[start]:
            end -= 1
            start += 1
        else:
            return False
    return True


def removeElement(nums, val):
    i = 0
    write_pointer = 0
    while i < len(nums):
        if nums[i] != val:
            nums[i], nums[write_pointer] = nums[write_pointer], nums[i]
            write_pointer += 1
        i += 1
    return write_pointer


def twoSum(numbers, target):
    # dicts = {}
    # for i in range(1, len(numbers)):
    #     val = target - numbers[i - 1]
    #     if val in dicts:
    #         return [dicts[val], i]
    #     dicts[numbers[i - 1]] = i
    # return [-1, -1]
    left = 1
    right = len(numbers) - 1
    while left <= right:
        if numbers[left - 1] + numbers[right] > target:
            right -= 1
        elif numbers[left - 1] + numbers[right] < target:
            left += 1
        else:
            return [left, right + 1]
    return [-1, -1]


def moveZeroes(nums):
    end = len(nums) - 1
    start = 0
    while start <= end:
        if nums[end] == 0:
            end -= 1
        if nums[start] == 0:
            nums[start], nums[end] = nums[end], nums[start]
            end -= 1
        start += 1
    return nums


def sortedSquares(nums):
    num = [0] * len(nums)
    start = 0
    end = len(nums) - 1
    i = end
    while i > -1:
        print(start, end)
        if abs(nums[end]) < abs(nums[start]):
            num[i] = nums[start] ** 2
            start += 1
        else:
            num[i] = nums[start] ** 2
            end -= 1
        i -= 1

    print(num)


print(sortedSquares([-4, -1, 0, 3, 10]))
