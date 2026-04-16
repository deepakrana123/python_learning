def twoSum(nums, target):
    # for i in range(len(nums)):
    #     for j in range(i, len(nums)):
    #         if nums[i] + nums[j] == target:
    #             return [i, j]
    # return [-1, -1]
    # i = 0
    # j = len(nums) - 1
    # arr = [(num, idx) for idx, num in enumerate(nums)]
    # arr.sort()
    # while i < j:
    #     s = arr[i][0] + arr[j][0]
    #     if s == target:
    #         return [arr[i][1], arr[j][1]]
    #     elif s < target:
    #         i += 1
    #     elif s > target:
    #         j -= 1
    # return [-1, -1]
    dict = {}
    for i in range(len(nums)):
        value = target - nums[i]
        if value in dict:
            return [dict[value], i]
        dict[nums[i]] = i
    return [-1, -1]


def lengthOfLongestSubstring(s):
    # i = 0
    # j = 0
    # result = 0
    # dicts = {}
    # while j < len(s):
    #     dicts[s[j]] = dicts.get(s[j], 0) + 1
    #     if dicts[s[j]] > 1:
    #         while dicts[s[j]] > 1:
    #             if s[i] in dicts:
    #                 dicts[s[i]] -= 1
    #                 if dicts[s[i]] == 0:
    #                     del dicts[s[i]]
    #                 i += 1
    #     result = max(result, j - i + 1)
    #     j += 1
    # return result
    # left = max_length = 0
    # char_set = set()
    # for right in range(len(s)):
    #     while s[right] in char_set:
    #         char_set.remove(s[left])
    #         left += 1
    #     char_set.add(s[right])
    #     max_length = max(max_length, right - left + 1)
    # return max_length
    # left=max_length=0
    # count={}
    # for right,value in enumerate(s):
    #     count[value]=count.get(value,0)+1
    #     while count[value]>1:
    #         count[s[left]]-=1
    #         left+=1
    #     max_length=max(max_length,right-left+1)
    # return max_length
    left = max_length = 0
    last_seen = {}
    for right, c in enumerate(s):
        if c in last_seen and last_seen(c) >= left:
            left = last_seen[c] + 1
        max_length = max(max_length, right - left + 1)
    return max_length


def subarraySum(nums, k):
    cummulativeSum = 0
    cummulativeDicts = {}
    cummulativeDicts[0] = 1
    result = 0
    for i in range(len(nums)):
        print(cummulativeSum, cummulativeDicts, "hlo")
        cummulativeSum += nums[i]
        val = cummulativeSum - k
        if val in cummulativeDicts:
            result += cummulativeDicts[val]
        if cummulativeSum in cummulativeDicts:
            cummulativeDicts[cummulativeSum] += 1
        else:
            cummulativeDicts[cummulativeSum] = 1
    return result


print(subarraySum([1, 1, 1], k=2))
