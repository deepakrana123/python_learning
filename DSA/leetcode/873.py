def lenLongestFibSubseq(arr):
    mp = {}

    def solve(j, k, arr, mp):
        a = arr[k] - arr[j]
        if a in mp and mp[a] < j:
            i = mp[a]
            return solve(i, j, arr, mp) + 1
        return 2

    maxResult = float("-inf")
    mp[arr[0]] = 0
    for i in range(len(arr)):
        mp[arr[i]] = i
    for j in range(1, len(arr)):
        for k in range(j + 1, len(arr)):
            length = solve(j, k, arr, mp)
            if length >= 3:
                maxResult = max(length, maxResult)
    return maxResult


print(lenLongestFibSubseq([1, 3, 7, 11, 12, 14, 18]))
