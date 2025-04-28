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


from collections import defaultdict


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


print(countInterestingSubarrays([3, 2, 4], modulo=2, k=1))
