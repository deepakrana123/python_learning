def countLargestGroup(n):
    dicts = {}
    groupMap = 0
    result = 0
    for i in range(1, n + 1):
        s = sum([int(x) for x in str(i)])
        dicts[s] = dicts.get(s, 0) + 1
        if dicts[s] == groupMap:
            result += 1
        elif dicts[s] > groupMap:
            result = 1
            groupMap = dicts[s]
    return result


def countGoodTriplets(arr, a, b, c):
    result = 0
    for i in range(0, len(arr) - 2):
        for j in range(i + 1, len(arr) - 1):
            for k in range(j + 1, len(arr)):
                if (
                    abs(arr[i] - arr[j]) <= a
                    and abs(arr[j] - arr[k]) <= b
                    and abs(arr[i] - arr[k]) <= c
                ):
                    result += 1
    return result


import math


def minimumOperations(nums):
    n = len(nums)
    st = set()
    for i in range(n - 1, -1, -1):
        if nums[i] in st:
            return math.ceil((i + 1) / 3)
        st.add(nums[i])
    return -1


def lca(root, dicts, maxD):
    if root == None or dicts[root] == maxD:
        return root
    leftN = lca(root.left, dicts, maxD)
    rightN = lca(root.right, dicts, maxD)
    if leftN and rightN:
        return root
    return leftN if rightN == None else rightN


def depth(root, dicts, dep, maxD):
    if root == None:
        return None
    maxD = max(maxD, depth)
    dicts[root] = dep
    depth(root.left, dicts, dep + 1, maxD)
    depth(root.right, dicts, dep + 1, maxD)


def lcaDeepestLeaves(root):
    dicts = {}
    maxD = 0
    depth(root, dicts, 0, maxD)


def countSubarrays(nums, k):
    i = 0
    j = 0
    sums = 0
    result = 0
    while j < len(nums):
        sums += nums[j]
        while sums * (j - i + 1) >= k:
            result += j - i + 1
            sums -= nums[i]
            i += 1
        j += 1
    return result
