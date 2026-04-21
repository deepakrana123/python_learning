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


def countDistinct(arr):
    # result = 0
    # for i in range(len(arr)):
    #     j = 0
    #     for j in range(i):
    #         if arr[i] == arr[j]:
    #             break
    #     if i == j + 1:
    #         result += 1

    # return result
    # arr.sort()
    # result = 1
    # for i in range(1, len(arr)):
    #     if arr[i] != arr[i - 1]:
    #         result += 1
    # return result
    print(len(set(arr)))
    result = set()
    for num in arr:
        if num not in result:
            result.add(num)
    return len(result)


# def findAnagrams(s, p):
#     dicts = {}
#     for i in range(0, len(s)):
#         abc = "".join(sorted(s[i : len(p)]))
#         print(abc, "abc")
#         if abc == "".join(sorted(p)):
#             if abc not in dicts:
#                 dicts[abc] = [i]
#             else:
#                 dicts[abc].append(i)
#     return dicts


def longestSubarray(arr):
    result = 0
    # for i in range(len(arr)):
    #     sums = arr[i]
    #     for j in range(i + 1, len(arr)):
    #         sums += arr[j]
    #         if sums == 0:
    #             result = max(result, j - i + 1)
    # return result
    dicts = {}
    prefixSum = 0
    dicts[prefixSum] = -1
    result = 0
    for i in range(len(arr)):
        prefixSum += arr[i]
        if prefixSum in dicts:
            prevIndex = dicts[prefixSum]
            length = i - prevIndex
            result = max(result, length)
        else:
            dicts[prefixSum] = i
    return result


from collections import Counter


def findAnagrams(s, p):
    # result = []
    # for i in range(len(s) - len(p) + 1):
    #     if sorted(s[i : i + len(p)]) == sorted(p):
    #         result.append(i)
    # return result
    # need = Counter(p)
    # window = {}
    # k = len(p)
    # ans = []
    # for j in range(len(s)):
    #     window[s[j]] = window.get(s[j], 0) + 1
    #     if j >= k:
    #         left = s[j - k]
    #         window[left] -= 1
    #         if window[left] == 0:
    #             del window[left]
    #     if window == need:
    #         ans.append(j - k + 1)
    # return ans
    if len(p) > len(s):
        return []
    need = [0] * 26
    window = [0] * 26
    for ch in p:
        need[ord(ch) - 97] += 1
    ans = []
    k = len(p)
    for j in range(len(s)):
        window[ord(ch) - 97] += 1
        if j >= k:
            window[ord(s[j - k]) - 97] -= 1
        if window == need:
            ans.append(j - k + 1)
    return ans


def countZeroSum(arr):
    # result = 0
    # for i in range(len(arr)):
    #     sums = arr[i]
    #     if arr[i] == 0:
    #         result += 1
    #     for j in range(i + 1, len(arr)):
    #         sums += arr[j]
    #         if sums == 0:
    #             result += 1

    # return result
    # dicts = {0: 1}
    # result = 0
    # sums = 0
    # for i in range(1, len(arr)):
    #     sums += arr[i]
    #     if sums in dicts:
    #         result += dicts[sums]
    #     dicts[sums] = dicts.get(sums, 0) + 1
    # return result
    n = len(arr)
    subarrays = [arr[i : j + 1] for i in range(n) for j in range(i, n)]
    count = sum(1 for sub in subarrays if sum(sub) == 0)
    return count


def leadersInArray(arr):
    # suffix = []
    # suffix.append(arr[-1])
    # for i in range(len(arr) - 2, -1, -1):
    #     if suffix[-1] <= arr[i]:
    #         suffix.append(arr[i])
    # return suffix[::-1]
    result = []
    n = len(arr)
    for i in range(n):
        for j in range(i + 1, n):
            if arr[i] < arr[j]:
                break
        else:
            result.append(arr[i])
    return result


print(leadersInArray([16, 17, 4, 3, 5, 2]))
