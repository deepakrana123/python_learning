def pivotArray(nums, pivot):
    arr = [pivot] * len(nums)
    j = 0
    countPivot = 0
    for num in nums:
        if num < pivot:
            arr[j] = num
            j += 1
        if num == pivot:
            countPivot += 1
    j = j + countPivot
    for num in nums:
        if num > pivot:
            arr[j] = num
            j += 1
    return arr


print(pivotArray([-3, 4, 3, 2], pivot=2))
