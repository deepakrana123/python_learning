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


def trap(height):
    n = len(height)
    total_water = 0
    # for i in range(n):
    #     left_max = 0
    #     for j in range(i + 1):
    #         left_max = max(left_max, height[j])
    #     right_max = 0
    #     for j in range(i, n):
    #         right_max = max(right_max, height[j])
    #     water = min(left_max, right_max) - height[i]
    #     if water > 0:
    #         total_water += water
    # return total_water
    # if n == 0:
    #     return 0
    # left_max = [0] * n
    # left_max[0] = height[0]
    # for i in range(1, n):
    #     left_max[i] = max(left_max[i - 1], height[i])
    # right_max = [0] * n
    # right_max[n - 1] = height[n - 1]
    # for i in range(n - 2, -1, -1):
    #     right_max[i] = max(right_max[i + 1], height[i])

    # for i in range(n):
    #     water = min(right_max[i], left_max[i]) - height[i]
    #     if water > 0:
    #         total_water += water
    # return total_water
    if n == 0:
        return 0
    if not height or len(height) < 3:
        return 0
    left = 0
    right = len(height) - 1
    left_max = height[left]
    right_max = height[right]
    total_water = 0
    while left < right:
        if left_max < right_max:
            left += 1
            left_max = max(left_max, height[left])
            water = left_max - height[left]
            if water > 0:
                total_water += water
        else:
            right -= 1
            right_max = max(right_max, height[right])
            water = right_max - height[right]
            if water > 0:
                total_water += water
    return total_water


def majorityElement(nums):
    # dicts = {}
    # for num in nums:
    #     dicts[num] = dicts.get(num, 0) + 1
    # for key, value in dicts.items():
    #     if value > len(nums) // 2:
    #         return key
    # return -1
    count = 0
    candidate = 0
    for num in nums:
        print(f"{num} num {count} count {candidate} candidate is good")
        if count == 0:
            count += 1
            candidate = num
        elif candidate == num:
            count += 1
        else:
            count -= 1
    return candidate


def search(nums, target):
    start = 0
    end = len(nums) - 1
    while start <= end:
        mid = start + (end - start) // 2
        print(f"{start} {end} {mid} ")
        if nums[mid] == target:
            return mid
        if nums[mid] >= nums[start]:
            if nums[start] <= target < nums[mid]:
                end = mid - 1
            else:
                start = mid + 1
        else:
            if nums[mid] < target <= nums[end]:
                start = mid + 1
            else:
                end = mid - 1
    return -1


def findMedianSortedArrays(nums1, nums2):
    # nums = nums1 + nums2
    # nums.sort()
    # n = len(nums)
    # if n % 2 == 0:
    #     return (nums[n // 2 - 1] + nums[n // 2]) / 2.0
    # return nums[n // 2]
    m = len(nums1)
    n = len(nums2)
    i = 0
    j = 0
    m1 = -1
    m2 = -1
    for count in range((m + n) // 2 + 1):
        m2 = m1
        if i != m and j != n:
            if nums1[i] > nums2[j]:
                m1 = nums2[j]
                j += 1
            else:
                m1 = nums1[i]
                i += 1
        elif i < m:
            m1 = nums1[i]
            i += 1
        else:
            m1 = nums2[j]
            j += 1
    return m1 if (m + n) % 2 == 1 else (m1 + m2) / 2.0


print(findMedianSortedArrays([1, 3], nums2=[2]))
