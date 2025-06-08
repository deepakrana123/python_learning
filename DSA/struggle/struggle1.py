import heapq


def dfs(graph, word, visited):
    visited[ord(word) - ord("a")] = 1
    minChar = word
    if word not in graph:
        return word
    for v in graph[word]:
        if visited[ord(v) - ord("a")] == 0:
            minChar = min(dfs(graph, v, visited), minChar)
    return minChar


def smallestEquivalentString(s1, s2, baseStr):
    if len(s1) != len(s2):
        return None
    graph = {}
    for i in range(len(s1)):
        if s1[i] not in graph:
            graph[s1[i]] = []
        if s2[i] not in graph:
            graph[s2[i]] = []
        graph[s1[i]].append(s2[i])
        graph[s2[i]].append(s1[i])

    strs = ""
    print(graph)
    for word in baseStr:
        visited = [0] * 26
        strs += dfs(graph, word, visited)
    return strs


def answerString(word, numFriends):
    n = len(word)
    result = ""
    longestPossible = n - numFriends + 1
    for i in range(n):
        canTakeLength = min(longestPossible, n - 1)
        result = max(result, word[i:canTakeLength])
    return result


def sortedSquares(nums):
    left = 0
    right = len(nums) - 1
    result = [0] * len(nums)
    for i in range(len(nums)):
        if abs(nums[left]) > abs(nums[right]):
            result[i] = nums[left] ** 2
            left += 1
        else:
            result[i] = nums[right] ** 2
            right -= 1
    return result[::-1]


def findLeastNumOfUniqueInts(arr, k):
    dicts = {}
    for i in range(len(arr)):
        dicts[arr[i]] = dicts.get(arr[i], 0) + 1
    heap = []
    for key in dicts:
        heapq.heappush(heap, (dicts[key], key))
    while k > 0:
        a, b = heapq.heappop(heap)
        if a - 1 != 0:
            heapq.heappush(heap, (a - 1, b))
        k -= 1
    return len(heap)


def commonChars(words):
    dicts1 = {}
    for w in words[0]:
        dicts1[w] = dicts1.get(w, 0) + 1
    print(dicts1, "dicts1")
    for i in range(1, len(words)):
        dicts2 = {}
        for key in words[i]:
            dicts2[key] = dicts2.get(key, 0) + 1
        for w in dicts1:
            if w in dicts2:
                dicts1[w] = min(dicts1[w], dicts2[w])
            else:
                dicts1[w] = 0
    abc = []
    for key in dicts1:
        if dicts1[key] != 0:
            abc.append(key)
    return abc


def relativeSortArray(arr1, arr2):
    dicts1 = {}
    for w in arr1:
        dicts1[w] = dicts1.get(w, 0) + 1
    abc = []
    for i in range(len(arr2)):
        if arr2[i] in dicts1:
            for _ in range(dicts1[arr2[i]]):
                abc.append(arr2[i])
    return abc


def heightChecker(heights):
    expected = sorted(heights)
    count = 0
    for i in range(len(heights)):
        if heights[i] != expected[i]:
            count += 1
    return count


def buyChoco(prices, money):
    prices.sort()
    a = money - (prices[0] + prices[1])
    if a >= 0:
        return a
    else:
        return money


def lastNonEmptyString(s):
    seens = set()
    stack = []
    for word in s:
        if word in seens:
            stack.append(word)
            break
        seens.add(word)
        stack.append(word)
    target = ".".join(stack)
    result = []
    remove = False
    i = 0
    while i < len(s):
        if not remove and s[i : i + len(target)] == target:
            i += len(target)
            remove = True
        else:
            result.append(s[i])
            i += 1
    print(result, "result")


def checkColumns(arr, col):
    sums = 0
    for i in range(len(arr)):
        sums += arr[i][col]
    return sums == 1


def checkRows(arr, row):
    sums = 0
    for j in range(len(arr[0])):
        sums += arr[row][j]
    return sums == 1


def numSpecial(mat):
    count = 0
    for i in range(len(mat)):
        for j in range(len(mat[0])):
            if mat[i][j] == 1:
                if checkColumns(mat, j) and checkRows(mat, i):
                    count += 1
    return count


print(numSpecial([[1, 0, 0], [0, 0, 1], [1, 0, 0]]))


def lastNonEmptyString(s):
    dicts = {}
    dicts2 = {}
    maxs = 0
    for w in range(len(s)):
        dicts[s[w]] = dicts.get(s[w], 0) + 1
        maxs = max(dicts[s[w]], maxs)
        dicts2[s[w]] = w
    sts = ""
    ab = set()
    for key in dicts:
        if dicts[key] == maxs:
            ab.add(key)
    for i in range(len(s) - 1, -1, -1):
        if s[i] in ab and s[i] not in sts:
            sts += s[i]
            if len(sts) == len(ab):
                break
    return sts[::-1]


def returnToBoundaryCount(nums):
    count = 0
    sums = 0
    for num in nums:
        sums += num
        if sums == 0:
            count += 1
    return count


def numOfUnplacedFruits(fruits, baskets):
    count = 0
    for i in range(len(fruits)):
        for j in range(len(baskets)):
            if fruits[i] < baskets[j]:
                count += 1
                break
    return len(fruits) - count if count > 0 else 0


def arrayStringsAreEqual(word1, word2):
    return "".join(word1) == "".join(word2)


def largestGoodInteger(num):
    count = -1
    maxStr = ""
    for i in range(2, len(num)):
        if num[i - 1] == num[i] == num[i + 1]:
            if count < int(num[i]):
                count = int(num[i])
    for _ in range(3):
        if count != -1:
            maxStr += str(count)
    return maxStr


def numberOfSpecialChars(word):
    lowers = set()
    higher = set()
    for w in word:
        if w.islower():
            lowers.add(w)
        if w.isupper():
            higher.add(w)
    count = 0
    for key in lowers:
        if key.upper() in higher:
            count += 1
    return count


# def getLargestOutlier(nums):
def sortVowels(s):
    arr = []
    vowel = set("aeiouAEIOU")
    t = list(s)
    for i in range(len(s)):
        if s[i] in vowel:
            arr.append(s[i])
    arr.sort()
    j = 0
    for i in range(len(s)):
        if s[i] in vowel:
            t[i] = arr[j]
            j += 1
    return "".join(t)


def groupAnagrams(strs):
    dicts = {}
    for i in range(len(strs)):
        rev = "".join(sorted(strs[i]))
        if rev in dicts:
            dicts[rev].append(strs[i])
        else:
            dicts[rev] = [strs[i]]
    return list(dicts.values())


def isPossibleDivide(nums, k):
    if len(nums) % k != 0:
        return False
    dicts = {}
    for num in nums:
        dicts[num] = dicts.get(num, 0) + 1
    # while dicts:
    #     first_key = next(iter(sorted(dicts.items())))
    #     for i in range(k):
    #         value = first_key[0] + i
    #         if value not in dicts or dicts[value] == 0:
    #             return False
    #         dicts[value] = dicts[value] - 1
    #         if dicts[value] == 0:
    #             del dicts[value]
    # return True
    for num in sorted(dicts):
        if dicts[num] > 0:
            freq = dicts[num]
            for i in range(k):
                if dicts[num + i] < freq:
                    return False
                dicts[num + i] -= freq
    return True


import heapq


def clearStars(s):
    stack = []
    heap = []
    deleted = set()

    for i, ch in enumerate(s):
        if ch != "*":
            stack.append((s[i], i))
            heapq.heappush(heap, (s[i], -i))
        else:
            while heap:
                char, index = heapq.heappop(heap)
                if -1 * index not in deleted:
                    deleted.add(-1 * index)
                    break
    result = [char for char, indx in stack if indx not in deleted]
    return "".join(result)


print(clearStars("abc"))
