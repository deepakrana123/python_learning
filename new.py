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

    def add(self, userId: int, taskId: int, priority: int) -> None:
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
