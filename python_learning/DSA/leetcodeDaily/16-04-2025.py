from collections import defaultdict


def countGood(nums, k):
    i = 0
    j = 0
    n = len(nums)
    dicts = {}
    pairs = 0
    result = 0
    while j < n:
        pairs += dicts[nums[j]] if nums[j] in dicts else 0
        dicts[nums[j]] = dicts.get(nums[j], 0) + 1

        while pairs >= k:
            result += n - j
            dicts[nums[j]] -= 1
            pairs -= dicts[nums[j]]
            i += 1
        j += 1
    return result


def countCompleteSubarrays(nums):
    m = {}
    for num in nums:
        m[num] = m.get(num, 0) + 1
    result = 0
    j = 0
    i = 0
    ansMap = {}
    while j < len(nums):
        ansMap[nums[j]] = ansMap.get(nums[j], 0) + 1
        while len(ansMap) == len(m):
            result += len(nums) - j
            ansMap[nums[i]] = ansMap.get(nums[i]) - 1
            if ansMap[nums[i]] == 0:
                del ansMap[nums[i]]
            i += 1
        j += 1
    return result


def countInterestingSubarrays(nums, modulo, k):
    for i in range(len(nums)):
        nums[i] = 1 if nums[i] % modulo == k else 0
    prefix_sum = 0
    count = 0
    freq = defaultdict(int)
    freq[0] = 1
    for num in nums:
        prefix_sum = (prefix_sum + num) % modulo
        target = (prefix_sum - k + modulo) % modulo
        count += freq[target]
        freq[prefix_sum] += 1
    return count


def countSubarrays(nums, k):
    i = 0
    j = 0
    maxs = max(nums)
    count = 0
    result = 0
    while j < len(nums):
        if nums[j] == maxs:
            count += 1
        while count >= k:
            result += len(nums) - j
            if nums[i] == maxs:
                count -= 1
            i += 1
        j += 1
    return result


def buildArray(nums):
    a = [-1] * len(nums)
    for i in range(len(nums)):
        a[i] = nums[nums[i]]
    return a


def minSum(nums1, nums2):
    s1 = sum(nums1) + nums1.count(0)
    s2 = sum(nums2) + nums2.count(0)
    zeroinnums1 = nums1.count(0)
    zeroinnums2 = nums2.count(0)
    if s1 < s2 and zeroinnums1 == 0:
        return -1
    if s1 > s2 and zeroinnums2 == 0:
        return -1
    return max(s1, s2)


def findEvenNumbers(digits):
    abc = set()
    for i in range(len(digits)):
        a = [0] * 3
        a.append(digits[i])
        for j in range(len(digits)):
            if i != j and len(a) != 3:
                a.append(digits[i])
            if len(a) == 3 and a[-1] % 2 == 0:
                abc.add(",".join(a))
    print(abc)


def lengthAfterTransformations(s, t):
    # dicts = {}
    # for u in s:
    #     dicts[u] = dicts.get(u, 0) + 1
    # mod = pow(10, 9) + 7
    # for i in range(1, t + 1):
    #     d = defaultdict(int)
    #     for key in dicts:
    #         if key != "z":
    #             next_char = chr(ord(key) + 1)
    #             d[next_char] = (d[next_char] + dicts[key]) % mod
    #         else:
    #             d["a"] = (d["a"] + dicts[key]) % mod
    #             d["b"] = (d["b"] + dicts[key]) % mod
    #     dicts = d
    # return sum(dicts.values()) % mod
    mod = 10**9 + 7
    freq = [0] * 26
    for ch in s:
        freq[ord(ch) - ord("a")] += 1

    for _ in range(t):
        new_freq = [0] * 26
        for i in range(25):
            new_freq[i + 1] = (new_freq[i + 1] + freq[i]) % mod
        z_count = freq[25]
        new_freq[0] = (new_freq[0] + z_count) % mod
        new_freq[1] = (new_freq[1] + z_count) % mod
        freq = new_freq
    return sum(freq) % mod


print(lengthAfterTransformations("abcyy", t=2))
