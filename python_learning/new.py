def numSubmatrixSumTarget(matrix, target=0):
    result = 0
    for i in range(len(matrix)):
        for j in range(1, len(matrix[0])):
            matrix[i][j] = matrix[i][j] + matrix[i][j - 1]
    for start_cols in range(len(matrix[0])):
        for j in range(start_cols, len(matrix[0])):
            maps = {0: 1}
            cumSum = 0
            for i in range(len(matrix)):
                cumSum += matrix[i][j] - (
                    matrix[i][start_cols - 1] if start_cols > 0 else 0
                )
                if cumSum - target in maps:
                    result += maps.get(cumSum - target, 0)
                maps[cumSum] = maps.get(cumSum, 0) + 1
    return result


def minimumTeachings(n, languages, friendships):
    sadUsers = set()
    for u, v in friendships:
        canTalk = False
        for lan_v in languages[v - 1]:
            if lan_v in languages[u - 1]:
                canTalk = True
                break
        if not canTalk:
            sadUsers.add(u)
            sadUsers.add(v)

    language = [0] * (n + 1)
    mostKnowLangauge = 0
    for user in sadUsers:
        for lang in languages[user - 1]:
            language[lang] += 1
            mostKnowLangauge = max(language[lang], mostKnowLangauge)
    return len(sadUsers) - mostKnowLangauge


def maxFreqSum(s):
    evenSum = 0
    consonantSum = 0
    dicts = {}
    for value in s:
        if value in "aeiou":
            dicts[value] = dicts.get(value, 0) + 1
            evenSum = max(dicts[value], evenSum)
        else:
            dicts[value] = dicts.get(value, 0) + 1
            consonantSum = max(dicts[value], consonantSum)
    return consonantSum + evenSum


def doesAliceWin(s):
    dicts = {}
    for value in s:
        if value in "aeiou":
            dicts[value] = dicts.get(value, 0) + 1
    if len(dicts) == 0:
        return False
    return True


def majorityElement(nums):
    candidate = 0
    count = 0
    for num in nums:
        if count == 0:
            candidate, count = num, 1
        elif candidate == num:
            count += 1
        else:
            count -= 1
    print(num, candidate)
    return candidate


from collections import deque


def firstUniqChar(s):
    queue = deque()
    maps = {}
    for i in range(len(s)):
        maps[s[i]] = maps.get(s[i], 0) + 1
        queue.append([s[i], i])

        while len(queue) > 0 and maps[queue[0][0]] > 1:
            queue.popleft()
    return queue[0][1] if queue else -1


def minDeletions(s):
    maps = {}
    for i in range(len(s)):
        maps[s[i]] = maps.get(s[i], 0) + 1
    sorted_items = sorted(maps.values(), reverse=True)
    sets = set()
    result = 0
    for value in sorted_items:
        while value > 0 and value in sets:
            result += 1
            value -= 1
        if value > 0:
            sets.add(value)
    return result


def minSteps(s, t):
    if len(s) != len(t):
        return 0
    maps = {}
    for i in range(len(s)):
        maps[s[i]] = maps.get(s[i], 0) + 1

    result = 0
    for value in t:
        if value in maps:
            maps[value] = maps.get(value, 0) - 1
            if maps[value] == 0:
                del maps[value]
        else:
            result += 1
    return result


def minSteps(s, t):
    maps1 = {}
    maps2 = {}
    for i in range(len(s)):
        maps1[s[i]] = maps1.get(s[i], 0) + 1
        maps2[t[i]] = maps2.get(t[i], 0) + 1

    result = 0
    for i in range(len(t)):
        if t[i] in maps1:
            maps1[t[i]] = maps1.get(t[i], 0) - 1
            if maps1[t[i]] == 0:
                del maps1[t[i]]
        if s[i] in maps2:
            maps2[s[i]] = maps2.get(s[i], 0) - 1
            if maps2[s[i]] == 0:
                del maps2[s[i]]
        else:
            result += 1
    return result


# def wordPattern(pattern, s):
#     maps1 = {}
#     maps2 = {}
#     for i in range(len(s)):
#         if s[i] not in maps1:
#             maps1[s[i]]=pattern[i]
#             maps2[pattern[i]]=map


def spellchecker(wordlist, queries):
    sets = set(wordlist)
    maps = {}
    for i in range(len(wordlist)):
        small = wordlist[i].lower()
        small1 = [key for key in small]
        if small in maps:
            continue
        maps[small] = wordlist[i]
        for j in range(len(small1)):
            if small1[j] in "aeiou":
                small1[j] = "*"
        masked = "".join(small1)
        if masked in maps:
            continue
        maps[masked] = wordlist[i]
    result = []
    for i in range(len(queries)):
        small = queries[i].lower()
        small1 = [key for key in small]
        for j in range(len(small1)):
            if small1[j] in "aeiou":
                small1[j] = "*"
        masked = "".join(small1)
        if queries[i] in sets:
            result.append(queries[i])
        elif small in maps:
            result.append(maps[small])
        elif masked in maps:
            result.append(maps[masked])
        else:
            result.append("")
    return result


from collections import Counter


def findCommonResponse(responses):
    # for i in range(len(responses)):
    #     maps = {}
    #     for j in range(len(responses[i])):
    #         if responses[i][j] in maps:
    #             responses[i][j] = "_"
    #         maps[responses[i][j]] = 1
    # result = {}
    # candidate = ""
    # count = 0
    # for i in range(len(responses)):
    #     for j in range(len(responses[i])):
    #         result[responses[i][j]] = result.get(responses[i][j], 0) + 1
    #         if responses[i][j] == "_":
    #             continue
    #         if result[responses[i][j]] > count:
    #             count = result[responses[i][j]]
    #             candidate = responses[i][j]
    #         elif count == result[responses[i][j]]:
    #             if candidate > responses[i][j]:
    #                 candidate = responses[i][j]

    # return candidate
    counter = Counter()

    for row in responses:
        counter.update(set(row))
    maxCount = max(counter.values())
    candidate = [word for word, c in counter.items() if c == maxCount]
    return min(candidate)


def numJewelsInStones(jewels: str, stones: str):
    count = 0
    for i in range(len(stones)):
        if stones[i] in jewels:
            count += 1
    return count


def uniqueMorseRepresentations(words):
    abc = set()
    count = 0
    morse_code = [
        ".-",
        "-...",
        "-.-.",
        "-..",
        ".",
        "..-.",
        "--.",
        "....",
        "..",
        ".---",
        "-.-",
        ".-..",
        "--",
        "-.",
        "---",
        ".--.",
        "--.-",
        ".-.",
        "...",
        "-",
        "..-",
        "...-",
        ".--",
        "-..-",
        "-.--",
        "--..",
    ]

    for value in words:
        strs = ""
        for v in value:
            strs += morse_code[ord(v) - ord("a")]
        if strs in abc:
            count += 1
        abc.add(strs)
    return count


def findWords(words):
    abc = ["qwertyuiop", "asdfghjkl", "zxcvbnm"]
    result = []

    def is_set_subset(word, row):
        for v in word:
            if v.lower() not in row:
                return False
        return True

    for word in words:
        for row in abc:
            if set(word.lower()).issubset(set(row)):
                result.append(word)
                break

    return result


def minDistance(word1, word2):
    dp = [[-1 for _ in range(len(word2))] for _ in range(len(word1))]

    def lcs(i, j):
        if i >= len(word1) or j >= len(word2):
            return 0
        if dp[i][j] != -1:
            return dp[i][j]

        if word1[i] == word2[j]:
            dp[i][j] = 1 + lcs(i + 1, j + 1)
            return dp[i][j]
        dp[i][j] = max(lcs(i + 1, j), lcs(i, j + 1))
        return dp[i][j]

    lcs_length = lcs(0, 0)
    return (len(word1) - lcs_length) + (len(word2) - lcs_length)


def compress(chars):
    n = len(chars)
    # j = 0
    # count = 1
    # result = ""
    # while j < n:
    #     while j + 1 < n and chars[j] == chars[j + 1]:
    #         count += 1
    #         j += 1
    #     result += chars[j] + (str(count) if count > 1 else "")
    #     j += 1
    #     count = 1
    # return result
    read = 0
    write = 0
    while read < n:
        char = chars[read]
        count = 0
        while read < n and char == chars[read]:
            read += 1
            count += 1

        chars[write] = char
        write += 1

        if count > 1:
            for v in str(count):
                chars[write] = v
                write += 1
    return chars


def removeDuplicateLetters(s):
    from collections import Counter

    last_occurrence = {c: i for i, c in enumerate(s)}
    stack = []
    lastSeen = set()
    for i in range(1, len(s)):
        if s[i] in lastSeen:
            continue

        while stack and stack[-1] > s[i] and i < last_occurrence[stack[-1]]:
            a = stack.pop()
            lastSeen.remove(a)
        stack.append(s[i])
        lastSeen.add(s[i])
    return "".join(stack)


def replaceNonCoprimes(nums):
    def gcd(x, y):
        while y:
            x, y = y, x % y
        return x

    def lcm(x, y):
        return abs(x * y) // gcd(x, y)

    stack = []
    for i in range(len(nums)):
        curr = nums[i]
        while stack:
            prev = stack[-1]
            if gcd(prev, curr) == 1:
                break
            stack.pop()
            curr = lcm(prev, curr)
        stack.append(curr)
    return stack


import heapq


def maxProfitAssignment(difficulty, profit, worker):
    heap = []
    result = 0
    for i in range(len(difficulty)):
        heapq.heappush(heap, (-profit[i], difficulty[i]))
    worker.sort(reversed=True)
    for i in range(len(worker)):
        while heap:
            profit, difficult = heapq.heappop(heap)
            if worker[i] >= difficult:

                result += -1 * profit
                heapq.heappush(heap, (profit, difficult))
                break
    return result
    # jobs = list(zip(difficulty, profit))
    # jobs.sort()
    # worker.sort()


class TaskManager:

    def __init__(self, tasks):
        self.tasks_proiroty = {}
        self.tasks_user = {}
        self.heap = []
        for user, tasks, priority in tasks:
            self.add(user, tasks, priority)

    def add(self, userId, taskId: int, priority: int) -> None:
        self.tasks_user[taskId] = userId
        self.task_proiroty[taskId] = priority
        heapq.heappush(self.heap, (-priority, taskId))

    def edit(self, taskId: int, newPriority: int) -> None:
        self.task_proiroty[taskId] = newPriority
        heapq.heappush(self.heap, (-newPriority, taskId))

    def rmv(self, taskId: int) -> None:
        self.task_proiroty[taskId] = -1

    def execTop(self) -> int:
        while self.heap:
            priority, task_id = heapq.heappop()
            newPrioirty = -1 * priority
            if newPrioirty == self.task_proiroty[task_id]:
                self.task_proiroty[task_id] = -1
                return self.tasks_user[task_id]
        return -1


class Spreadsheet:

    def __init__(self, rows: int):
        self.matrix = [[0 for _ in rows] for _ in 26]

    def setCell(self, cell: str, value: int) -> None:
        col = cell[0] - "A"
        row = int(cell[1:]) - 1
        self.matrix[col][row] = value

    def resetCell(self, cell: str) -> None:
        col = cell[0] - "A"
        row = int(cell[1:]) - 1
        self.matrix[col][row] = 0

    def solve(self, s):
        if s[0].isdigit():
            return s[0]
        col = s[0] - "A"
        row = int(s[1:]) - 1
        return self.matrix[col][row]

    def getValue(self, formula: str) -> int:
        s = formula[1:]
        plusIndex = s.find("+")
        leftStr = s[0:plusIndex]
        rightStr = s[plusIndex + 1 :]
        return self.solve(leftStr) + self.solve(rightStr)


from collections import deque


class Router:
    def __init__(self, memoryLimit):
        self.queue = deque()
        self.dicts_map = {}
        self.memoryLimit = memoryLimit
        self.source_time = {}

    def addPacket(self, source: int, destination: int, timestamp: int):
        creadted_str = str(source) + "_" + str(destination) + "_" + str(timestamp)
        if source not in self.source_time:
            self.source_time[source] = []
        self.source_time[source].append(timestamp)
        if creadted_str in self.dicts_map:
            return False
        if len(self.queue) >= self.memoryLimit:
            self.forwardPacket()
        self.dicts_map[creadted_str] = {
            source: source,
            destination: destination,
            timestamp: timestamp,
        }
        self.queue.append(creadted_str)
        return True

    def lower_bound(self, arr, target):
        left, right = 0, len(arr)
        while left < right:
            mid = (left + right) // 2
            if arr[mid] < target:
                left = mid + 1
            else:
                right = mid
        return left

    def upper_bound(self, arr, target):
        left, right = 0, len(arr)
        while left < right:
            mid = (left + right) // 2
            if arr[mid] <= target:
                left = mid + 1
            else:
                right = mid
        return left

    def forwardPacket(self):
        if not self.dicts_map:
            return {}
        queue_str = self.queue.popleft()
        packDeatils = self.dicts_map[queue_str]
        self.source_time[packDeatils["source"]].remove(packDeatils["timestamp"])
        if not self.source_time[packDeatils["source"]]:
            del self.source_time[packDeatils["source"]]
        del self.dicts_map[queue_str]
        return packDeatils

    def getCount(self, destination: int, startTime: int, endTime: int):
        values = self.source_time.get(destination, [])
        values.sort()
        lowerbound = self.lower_bound(values, startTime)
        upperbound = self.upper_bound(values, endTime)
        return upperbound - lowerbound + 1


class MovieRentingSystem:

    # def __init__(self, n, entries):
    #     self.available = {}
    #     self.rented = []
    #     self.shop_basis = {}
    #     for shop, movie, price in entries:
    #         if movie not in self.available:
    #             self.available[movie] = []
    #             self.shop_basis[movie] = {}
    #         self.shop_basis[movie][shop] = price
    #         self.available[movie].append([price, shop])

    # def search(self, movie: int):
    #     if movie not in self.available:
    #         return []
    #     movie_list = sorted(self.available[movie], key=lambda x: (x[0], x[1]))
    #     result = []

    #     for price, shop in movie_list[:5]:
    #         result.append(shop)
    #     return result

    # def rent(self, shop, movie):
    #     price = self.shop_basis[movie][shop]
    #     self.available[movie] = [x for x in self.available[movie] if x[1] != shop]
    #     self.rented.append([price, shop, movie])

    # def drop(self, shop, movie):
    #     price = self.shop_basis[movie][shop]
    #     self.rented = [x for x in self.rented if not (x[1] == shop and x[2] == movie)]
    #     self.available[movie].append([price, shop])

    # def report(self):
    #     rented_list = sorted(self.rented, key=lambda x: (x[0], x[1], x[2]))
    #     result = []
    #     for price, shop, movie in rented_list[:5]:
    #         result.append([shop, movie])
    #     return result
    import bisect


import bisect


class MovieRentingSystem:
    def __init__(self, n, entries):
        self.available = {}
        self.rented = []
        self.shop_basis = {}

        for shop, movie, price in entries:
            if movie not in self.available:
                self.available[movie] = []
                self.shop_basis[movie] = {}
            self.available[movie].append([price, shop])
            self.shop_basis[movie][shop] = price

        for movie in self.available:
            self.available[movie].sort()

    def search(self, movie: int):
        if movie not in self.available:
            return []
        return [shop for price, shop in self.available[movie][:5]]

    def rent(self, shop, movie):
        price = self.shop_basis[movie][shop]
        idx = bisect.bisect_left(self.available[movie], [price, shop])
        if idx < len(self.available[movie]) and self.available[movie][idx] == [
            price,
            shop,
        ]:
            self.available[movie].pop(idx)
        bisect.insort(self.rented, [price, shop, movie])

    def drop(self, shop, movie):
        price = self.shop_basis[movie][shop]
        idx = bisect.bisect_left(self.rented, [price, shop, movie])
        if idx < len(self.rented) and self.rented[idx] == [price, shop, movie]:
            self.rented.pop(idx)
        bisect.insort(self.available[movie], [price, shop])

    def report(self):
        return [[shop, movie] for price, shop, movie in self.rented[:5]]


import re


def mostCommonWord(paragraph, banned):
    words = ""
    maxCount = 0
    count = {}
    words1 = re.findall(r"\w+", paragraph.lower())
    for word in words1:
        if word in banned:
            continue
        count[word] = count.get(word, 0) + 1
        if maxCount < count[word]:
            maxCount = count[word]
            words = word
    return words


def topStudents(positive_feedback, negative_feedback, report, student_id, k):
    student_score = {}
    for i in range(len(report)):
        word = report[i].split(" ")
        for w in word:
            if w in positive_feedback:
                student_score[student_id[i]] = student_score.get(student_id[i], 0) + 3
            elif w in negative_feedback:
                student_score[student_id[i]] = student_score.get(student_id[i], 0) - 1

    sorted_keys = sorted(student_score.keys(), key=lambda k: (student_score[k], -k))[:k]
    return sorted_keys


class Solution:
    def compressInitial(self, s):
        r = 0
        for i in range(len(s)):
            if s[i] != 0:
                r = i
                break
        return s[r:]

    def compareVersion(self, version1: str, version2: str) -> int:
        a = version1.split(".")
        b = version2.split(".")
        if len(a) != len(b):
            return 0
        for i in range(len(a)):
            a[i] = self.compressInitial(a[i])
            b[i] = self.compressInitial(b[i])
        print(a, b)
        result = 0
        for i in range(len(a)):
            if int(a[i]) > int(b[i]):
                print(a[i], b[i])
                result = 1
            elif int(a[i]) < int(b[i]):
                result = -1
            else:
                result = 0
        return result


ac = Solution()
# print(ac.compareVersion("1.0", version2="1.0.0.0"))


def largestTriangleArea(points):
    result = 0
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            for k in range(j + 1, len(points)):
                x1, y1 = points[i]
                x2, y2 = points[j]
                x3, y3 = points[k]
                area = abs(0.5 * (x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)))
                result = max(result, area)
    return result


def triangleNumber(nums):
    # result = 0
    # for i in range(len(nums)):
    #     for j in range(i + 1, len(nums)):
    #         for k in range(j + 1, len(nums)):
    #             x1 = nums[i]
    #             x2 = nums[j]
    #             x3 = nums[k]
    #             if x1 + x2 > x3 and x1 + x3 > x2 and x2 + x3 > x1:
    #                 result += 1
    # return result
    result = 0
    n = len(nums)
    count = 0

    for k in range(n - 1, 1, -1):
        i, j = 0, k - 1
        while i < j:
            if nums[i] + nums[j] > nums[k]:
                count += j - i
                j -= 1
            else:
                i += 1
    return count


def largestPerimeter(self, nums):
    nums.sort()
    if len(nums) < 3:
        return 0
    for i in range(len(nums) - 3, -1, -1):
        if nums[i] + nums[i + 1] > nums[i + 2]:
            return nums[i + 1] + nums[i + 2] + nums[i]
    return 0


def triangularSum(nums):
    l = len(nums)
    while l > 1:
        i = 0
        while i < l - 1:
            nums[i] = (nums[i] + nums[i + 1]) % 10
            i += 1
        nums.pop()
        l = len(nums)
    return nums


def numWaterBottles(numBottles, numExchange):
    consumed = 0
    while numBottles >= numExchange:
        consumed += numExchange
        numBottles -= numExchange
        numBottles += 1
    return consumed + numBottles


def maxBottlesDrunk(numBottles, numExchange):
    emptyBottles = numBottles
    drunkBottles = numBottles
    while emptyBottles >= numExchange:
        emptyBottles -= numExchange
        numExchange += 1
        emptyBottles += 1
        drunkBottles += 1
    return drunkBottles


def missingInteger(nums):
    # maxLength = 0
    # resultsSum = 0
    # sets = set(nums)
    # for i in range(len(nums)):
    #     sums = nums[i]
    #     lengths = 1
    #     for j in range(i + 1, len(nums)):
    #         if nums[j - 1] + 1 == nums[j]:
    #             sums += nums[j]
    #             lengths += 1
    #         else:
    #             break
    #     if lengths > maxLength:
    #         maxLength = lengths
    #         resultsSum = sums

    # while resultsSum in sets:
    #     resultsSum += 1
    # return resultsSum
    num_set = set(nums)
    max_len = 0
    sum_of_longest = 0
    for num in nums:
        if num - 1 not in num_set:
            current = num
            current_sum = 0
            length = 0

            while current in num_set:
                current_sum += current
                length += 1
                current += 1
            if length > max_len:
                max_len = max(max_len, length)
                sum_of_longest = current_sum
    while sum_of_longest in num_set:
        sum_of_longest += 1
    return sum_of_longest


def maxCount(banned, n, maxSum):
    sets = set(banned)
    results = float("-inf")
    count = 0
    sums = 0
    for i in range(1, n + 1):
        if i not in sets:
            sums += i
            count += 1

        if maxSum > sums:
            results = max(count, results)
        else:
            sums = 0
            count = 0
    return results


def findDisappearedNumbers(nums):
    n = len(nums)
    results = []
    sets = set(nums)
    for i in range(1, n + 1):
        if i not in sets:
            results.append(i)
    return results


def findDuplicate(nums):
    i = 0
    while i < len(nums):
        correct_index = nums[i] - 1
        if nums[i] != nums[correct_index]:
            nums[i], nums[correct_index] = nums[correct_index], nums[i]
        else:
            i += 1
    return nums[-1]


def maximumSum(nums):
    dicts = {}

    def digitSum(num):
        abc = str(num)
        sums = 0
        for n in abc:
            sums += int(n)
        return sums

    for num in nums:
        abc = digitSum(num)
        if abc not in dicts:
            dicts[abc] = []
        dicts[abc].append(num)
    sums = [sum(value) for value in dicts.values()]
    return max(sums)


def zeroFilledSubarray(nums):
    i = 0
    j = 0
    result = 0
    while i < len(nums):
        if nums[j] != 0:
            i = j + 1
        result += j - i + 1
        j += 1
    return result


def solve(self, coins, amount, index):
    if index >= 0:
        if amount == 0:
            return 0
        else:
            return float("inf")
    skip = self.solve(coins, amount, index + 1)
    taken = 0
    if amount - coins[index] >= 0:
        taken = 1 + self.solve(coins, amount, index)
    return min(skip, taken)


from collections import deque


class Solution:
    def solve(self, coins, amount, index, dp):
        if index >= len(coins):
            if amount == 0:
                return 0
            else:
                return float("inf")
        if amount == 0:
            return 0
        if dp[index][amount] != -1:
            return dp[index][amount]
        taken = float("inf")
        skip = self.solve(coins, amount, index + 1, dp)
        if amount - coins[index] >= 0:
            taken = 1 + self.solve(coins, amount - coins[index], index, dp)
        dp[index][amount] = min(taken, skip)
        return min(taken, skip)

    def coinChange(self, coins, amount: int) -> int:
        dp = [[-1 for _ in range(amount + 1)] for _ in range(len(coins) + 1)]
        # a = self.solve(coins, amount, 0, dp)
        # return a if a != float("inf") else -1

        # for i in range(len(coins)):
        #     for j in range(1, amount + 1):
        #         if coins[i - 1] <= j:
        #             dp[i][j] = min(dp[i - 1][j], 1 + dp[i - 1][j - coins[i - 1]])
        #         else:
        #             dp[i][j] = dp[i - 1][j]

        if amount == 0:
            return 0

        queue = deque([0, 0])
        visited = set([0])
        while queue:
            current, steps = queue.popleft()
            for coin in coins:
                nxt = coin + current
                if nxt == amount:
                    return steps + 1
                if nxt < amount and nxt not in visited:
                    visited.add(nxt)
                    queue.append((nxt, steps + 1))
        return -1


def numIslands(grid):
    result = 0

    # def dfs(i, j):
    #     if i < 0 or i >= len(grid) or j < 0 or j >= len(grid[0]) or grid[i][j] == "0":
    #         return
    #     if grid[i][j] == -1:
    #         return
    #     grid[i][j] = -1
    #     dfs(i + -1, j + 0)
    #     dfs(i + 0, j - 1)
    #     dfs(i - 1, j - 1)
    #     dfs(i + 1, j + 1)

    # for i in range(len(grid)):
    #     for j in range(len(grid[0])):
    #         if grid[i][j] == "1":
    #             dfs(i, j)
    #             result += 1
    # return result

    if not grid:
        return 0

    rows, cols = len(grid), len(grid[0])
    result = 0
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    def bfs(i, j):
        queue = deque()
        queue.append((i, j))
        grid[i][j] = "0"

        while queue:
            x, y = queue.popleft()
            for _i, _j in directions:
                new_x = x + _i
                new_y = y + _j
                if (
                    new_x < 0
                    or new_x >= len(grid)
                    or new_y < 0
                    or new_y >= len(grid[0])
                    or grid[new_x][new_y] == "0"
                ):
                    return
                else:
                    grid[new_x][new_y] == "0"
                    queue.append((new_x, new_y))

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == "1":
                bfs(i, j)
                result += 1
    return result


def swimInWater(grid):
    m = len(grid)
    n = len(grid[0])

    # def dfs(i, j, time, visited):
    #     if (
    #         i < 0
    #         or i > m
    #         or j < 0
    #         or j > n
    #         or (i, j) in visited
    #         or grid[i][j] > time
    #     ):
    #         return False
    #     if i == m - 1 and j == n - 1:
    #         return True
    #     visited.add((i, j))

    #     for new_x, new_y in [(-1, 0), (0, -1), (0, 1), (1, 0)]:
    #         if dfs(new_x + i, new_y + j, time, visited):
    #             return True
    #     return False

    def canReach(i, j, time, visited):
        if grid[0][0] > time:
            return False
        stack = [(0, 0)]
        visited = set((0, 0))
        while stack:
            curr_i, curr_j = stack.pop()
            if curr_i == n - 1 and curr_j == n - 1:
                return True
            for new_x, new_y in [(-1, 0), (0, -1), (0, 1), (1, 0)]:
                if (
                    curr_i + new_x < 0
                    or curr_i + new_x > m
                    or curr_j + new_y < 0
                    or curr_j + new_y > n
                    or (curr_i + new_x, curr_j + new_y) in visited
                    or grid[curr_i + new_x][curr_j + new_y] > time
                ):
                    return False
                else:
                    visited(curr_i + new_x, curr_j + new_y)
                    stack.append((curr_i + new_x, curr_j + new_y))
        return False

    l = 0
    r = n * n - 1
    result = 0
    while l < r:
        visited = set()
        mid = l + (r - l) // 2
        if canReach(0, 0, mid, visited):
            result = mid
            r = mid - 1
        else:
            l = mid + 1
    return result


import heapq


def minOperations(nums, k):
    nums.sort()
    if nums[0] >= k:
        return 0
    if len(nums) == 1:
        if nums[0] >= k:
            return 0
        else:
            return -1

    heap = []
    for num in nums:
        heapq.heappush(heap, num)
    count = 0
    while len(heap) > 1:
        x = heapq.heappop(heap)
        y = heapq.heappop(heap)
        val = min(x, y) * 2 + max(x, y)
        count += 1
        if val < k:
            heapq.heappush(heap, val)
    if heap and heap[0] < k:
        return -1

    return count


def minAnagramLength(s):
    dicts = {}
    for n in s:
        dicts[n] = dicts.get(n, 0) + 1
    result = len(dicts)
    return result


def maximumEnergy(energy, k):
    dp = energy
    if len(energy) <= k:
        return max(energy)
    for i in range(len(energy) - k - 1, -1, -1):
        dp[i] = dp[i] + dp[i + k]
    return max(dp)


def avoidFlood(rains):
    ans = [-1] * len(rains)
    lake_map = {}
    dry_day = []

    def bs(arr, target):
        left = 0
        right = len(arr)
        while right > left:
            mid = left + (right - left) // 2
            if arr[mid] > target:
                right = mid
            else:
                left = mid + 1
        return left

    for i in range(len(rains)):
        if rains[i] == 0:
            dry_day.append(i)
        else:
            if rains[i] in lake_map:
                idx = bs(dry_day, lake_map[rains[i]])
                if idx == len(dry_day):
                    return []
                ans[dry_day[idx]] = rains[i]
                dry_day.pop(idx)
        lake_map[rains[i]] = i
    for i in dry_day:
        ans[i] = 1
    return ans


def removeAnagrams(words):
    dicts = {}
    for i in range(len(words)):
        abc = "".join(sorted(words[i]))
        if abc in dicts:
            words[i] = -1
        else:
            dicts[abc] = 1
    return [word for word in words if word != -1]


def hasIncreasingSubarrays(nums):
    n = len(nums)
    currRun = 1
    prevRun = 0
    result = 0
    for i in range(1, n):
        if nums[i] > nums[i - 1]:
            currRun + 1
        else:
            prevRun = currRun
            currRun = 1
        result = max(currRun // 2, result)
        result = max(min(currRun, prevRun), result)
    return result


def finalValueAfterOperations(operations):
    return sum(1 if "+" in op else -1 for op in operations)


def maxFrequency(nums, k, numOperations):
    maxEl = max(nums)
    freq = {}
    for num in nums:
        freq[num] = freq.get(num, 0) + 1

    for i in range(0, maxEl + 1):
        freq[i] = freq.get(i, 0) + 1
    result = 0
    for i in range(0, maxEl + 1):
        if freq[i] == 0:
            continue
        targetCount = (
            freq[i + k] if i + k in freq else 0 - freq[i - k] if i - k > 0 else 0
        )
        needConversion = freq[i] - freq[i - 1] if i - 1 > 0 else 0
        maxPossibleFreq = targetCount + min(targetCount - needConversion, numOperations)
        result = max(result, maxPossibleFreq)
    return result


# def minimumCost(target, words, costs):
# def solve(index, currString):
#     if index > len(words):
#         if currString == target:
#             return 0
#         return float("inf")
#     take = 0
#     if target.startswith(currString + words[index]):
#         take = costs[index] + solve(index + 1, currString + words[index])
#     skip = solve(index + 1, currString)
#     return min(take, skip)
# result = solve(0, "")
# if result == float("inf"):
#     return -1
# else:
#     result


def hasSameDigits(s):
    stack = []
    for i in range(1, len(s)):
        stack.append((int(s[i]) + int(s[i - 1])) % 10)
    while len(stack) > 2:
        stack = [(stack[i] + stack[i - 1]) % 10 for i in range(1, len(stack))]

    return stack[0] == stack[1] if len(stack) == 2 else False


def totalMoney(n):
    result = 0
    monday = 1
    while n > 0:
        money = monday
        for i in range(1, min(n, 7) + 1):
            result += money
            money += 1
        monday += 1
        n -= 7
    return result


def nextBeautifulNumber(n):
    result = 0

    def balance(num):
        result = [0] * 10
        while num > 0:
            digit = num % 10
            result[digit] += 1
            num = num // 10
        print(result, "result")
        for i in range(10):
            if result[i] > 0 and result[i] != i:
                return False
        return True

    for i in range(n, pow(10, 6) + 1):
        if balance(i):
            result = i
            break
    return result


class Bank:
    def __init__(self, balance):
        self.n = len(balance)
        self.balance = balance

    def transfer(self, account1: int, account2: int, money: int) -> bool:
        if account1 > self.n or account2 > self.n or account1 < 1 or account2 < 1:
            return False
        if self.balance[account1 - 1] >= money:
            self.balance[account2 - 1] += money
            self.balance[account1 - 1] -= money
            return True
        return False

    def deposit(self, account: int, money: int) -> bool:
        if account > self.n:
            return False
        self.balance[account - 1] += money
        return True

    def withdraw(self, account: int, money: int) -> bool:
        if account > self.n:
            return False
        if self.balance[account - 1] < money:
            return False
        self.balance[account - 1] -= money
        return True


def minNumberOperations(target):
    operations = 0
    prev = 0
    for i in range(len(target)):
        if prev < target[i]:
            operations += target[i] - prev
        prev = target[i]
    return operations


def mergeIntervalList(arr):
    results = [interval for sublist in arr for interval in sublist]
    if not results:
        return []

    results.sort(key=lambda x: x[0])

    merged = [results[0]]
    for i in range(1, len(results)):
        prev = merged[-1]
        curr = results[i]
        if prev[1] >= curr[0]:
            prev[1] = max(prev[1], curr[1])
        else:
            merged.append(curr)
    return merged


def findIntervalWithQueries(arr, queries):
    start = []
    end = []
    for i in range(len(arr)):
        start.append(arr[0])
        end.append(arr[1])
    start.sort()
    end.sort()

    def binarySearch(arr, value):
        start = 0
        end = len(arr)
        while start < end:
            mid = start + (end - start) // 2
            if arr[mid] < value:
                start = mid + 1
            else:
                end = mid
        return start

    result = []
    for i in range(len(queries)):
        count_start = binarySearch(start, queries[i])
        count_end = binarySearch(end, queries[i])
        result.append(count_end - count_start)
    return result


def taskScheduler(task, n):
    pass


def countUnguarded(self, m, n, guards, walls) -> int:
    arr = [[0 for _ in range(n)] for _ in range(m)]
    for k, l in guards:
        arr[k][l] = 1
    for i, j in walls:
        arr[i][j] = 2
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for gi, gj in guards:
        for di, dj in directions:
            i, j = gi, gj
            while 0 <= i + di < m and 0 <= j + dj < n:
                i += di
                j += dj
                if arr[i][j] == 2 or arr[i][j] == 1:
                    break
                if arr[i][j] == 0:
                    arr[i][j] = 3
    count = sum(arr[i][j] == 0 for i in range(m) for j in range(n))
    return count


import bisect


def jobScheduling(startTime, endTime, profit):
    arr = []
    arr = sorted(zip(startTime, endTime, profit), key=lambda x: x[1])
    dp = [0] * len(arr)
    ends = [job[1] for job in arr]
    dp[0] = arr[0][2]
    for i in range(1, len(arr)):
        take = arr[i][2]
        index = bisect.bisect_right(ends, arr[i][0]) - 1
        if index != -1:
            take += dp[index]
        skip = dp[i - 1]
        dp[i] = max(skip, take)
    return dp[-1]


def minimumTotalCost(arr):
    heap = []
    for i in range(len(arr)):
        heapq.heappush(heap, arr[i])
    cost = 0
    while heap and len(heap) >= 2:
        a = heapq.heappop(heap)
        b = heapq.heappop(heap)
        cost += a + b
        heapq.heappush(heap, a + b)
    return cost


def reorgnizeString(s):
    dicts = {}
    for strs in s:
        dicts[strs] = dicts.get(strs, 0) + 1
    heap = []
    for key in dicts:
        heapq.heappush(heap, (-dicts[key], key))
    result = ""
    while heap and len(heap) > 1:
        value1, str1 = heapq.heappop(heap)
        value2, str2 = heapq.heappop(heap)
        result += str1
        result += str1
        if value1 + 1 < 0:
            heapq.heappush(heap, (-(value1 + 1), str1))
        if value2 + 1 < 0:
            heapq.heappush(heap, (-(value2 + 1), str2))
    while heap:
        last, charlast = heapq.heappop(heap)
        if last == -1:
            result += charlast
        else:
            return ""
    return result


def ipo(k, w, profits, capital):
    arr = []
    for i in range(len(capital)):
        arr.append([capital[i], profits[i]])
    arr.sort(key=lambda x: x[0])
    heap = []
    i = 0
    for _ in range(k):
        while i < len(arr) and arr[i][0] <= w:
            heapq.heappush(heap, -arr[i][1])
        if not heap:
            break
        w += -heapq.heappop(heap)
    return w


def countOperations(num1, num2):
    count = 0
    while num1 > 0 and num2 > 0:
        if num1 >= num2:
            num1 = num1 - num2
        elif num2 > num1:
            num2 = num2 - num1
        count += 1
    return count


def findXSum(nums, k, x):
    i = 0
    j = 0
    dicts = {}

    def calculateMaxTwo(dicts):
        heap = []
        ans = 0
        for key in dicts:
            heapq.heappush(heap, (dicts[key], key))
            if len(heap) > x:
                heapq.heappop(heap)
        while heap:
            freq, num = heapq.heappop(heap)
            ans += num * freq
        return ans

    arr = []
    while j < len(nums):
        dicts[nums[j]] = dicts.get(nums[j], 0) + 1
        if j - i + 1 >= k:
            arr.append(calculateMaxTwo(dicts))
            dicts[nums[i]] = dicts[nums[i]] - 1
            if dicts[nums[i]] == 0:
                del dicts[nums[i]]
            i += 1
        j += 1
    return arr


import heapq


def networkDelayTime(times, n, k):
    heap = [(0, k)]
    dist = [float("inf")] * (n + 1)
    dist[k] = 0
    dist[0] = 0
    adj = {i: [] for i in range(1, n + 1)}
    for u, v, w in times:
        adj[u].append((v, w))
    while heap:
        curr_dist, node = heapq.heappop(heap)
        for ni, w in adj[node]:
            new_dist = curr_dist + w
            if ni not in dist and new_dist < dist[ni]:
                dist[ni] = new_dist
                heapq.heappush(heap, (new_dist, ni))

    return -1 if max(dist) == float("inf") else max(dist)


def swimInWater(grid):
    n = len(grid)
    left = 0
    right = n - 1
    result = 0

    def possibleToReach(grid, i, j, t, visited):
        if (
            i < 0
            or i >= n
            or j < 0
            or j >= n
            or visited[i][j] == True
            or grid[i][j] > t
        ):
            return True
        visited[i][j] = True
        if i == n - 1 and j == n - 1:
            return True

        for x, y in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
            i_ = i + x
            j_ = j + y
            if possibleToReach(grid, i_, j_, t, visited):
                return True
        return False

    while left <= right:
        mid = left + (right - left) // 2
        visited = [False for _ in range(n)] * n
        if possibleToReach(grid, 0, 0, mid, visited):
            result = mid
            right = mid - 1
        else:
            left = mid + 1
    return result


from collections import deque


def minimumEffortPath(heights):
    n, m = len(heights[0]), len(heights)
    # left = 0
    # right = float("-inf")
    # result = 0
    # for i in range(len(heights)):
    #     right = max(right, max(heights[i]))

    # def possibleToReach(grid, i, j, t, visited):

    #     if i == n - 1 and j == n - 1:
    #         return True
    #     visited[i][j] = True

    #     for x, y in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
    #         i_ = i + x
    #         j_ = j + y
    #         if i_ <= 0 or i_ > n or j_ <= 0 or j_ > n or visited[i][j] == False:
    #             if abs(grid[i_][j_] - grid[i][j]) <= t:
    #                 if possibleToReach(grid, i_, j_, t, visited):
    #                     return True
    #     return False

    # while left <= right:
    #     mid = left + (right - left) // 2
    #     visited = [False for _ in range(n)] * n
    #     if possibleToReach(heights, 0, 0, mid, visited):
    #         result = mid
    #         right = mid - 1
    #     else:
    #         left = mid + 1
    # return result
    dirs = [(-1, 0), (0, 1), (1, 0), (0, -1)]

    def canReach(threshold):
        q = deque([(0, 0)])
        visited = [[False] * n] * m
        visited[0][0] = True

        while q:
            x, y = q.popleft()
            if x == n - 1 and y == n - 1:
                return True
            for _x, _y in dirs:
                new_x, new_y = _x + x, _y + y
                if (
                    new_x <= 0
                    or new_x > n
                    or new_y <= 0
                    or new_y > n
                    or visited[new_x][new_y] == False
                ):
                    value = heights[new_x][new_y] - heights[x][y]
                    if value <= threshold:
                        visited[new_x][new_y] = True
                        q.append((new_x, new_y))
        return False

    left = 0
    right = max(max(row) for row in heights)
    while left <= right:
        mid = (left + right) // 2
        if canReach(mid):
            result = mid
            right = mid - 1
        else:
            left = mid + 1
    return result


from collections import defaultdict


def findCheapestPrice(n, flights, src: int, dst: int, k: int) -> int:
    heap = [(0, src, k + 1)]
    adj = [[] for _ in range(n + 1)]
    for u, v, w in flights:
        adj[u].append((v, w))
    dist = [[float("inf")] * (k + 2) for _ in range(n)]
    dist[src][k + 1] = 0

    while heap:
        current_dist, node, stops = heapq.heappop(heap)
        if node == dst:
            return current_dist
        if stops > 0:
            for v, weight in adj[node]:
                new_cost = current_dist + weight
                if new_cost < dist[v][stops - 1]:
                    heapq.heappush(heap, (current_dist + weight, v, stops - 1))

    return -1


def numSub(s):
    count = 0
    result = 0
    for i in range(len(s)):
        if s[i] == "0":
            result += (count * (count + 1)) // 2
            count = 0
        else:
            count += 1

    return result + (count * (count + 1)) // 2


def minimumOperations(nums):
    results = 0
    for num in nums:
        if num % 3 != 0:
            results += min(num % 3, 3 - (num % 3))
    return results
