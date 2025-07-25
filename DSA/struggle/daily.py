from collections import deque


def maxValue(events, k):
    events.sort(key=lambda x: x[0])
    dp = [[-1 for _ in range(k + 1)] for _ in range(len(events) + 1)]

    def linearSearch(events, index):
        start, end, weight = events[index]
        for i in range(index + 1, len(events)):
            if events[i][0] > end:
                return i
        return len(events)

    # def binarySearch(index):
    #     start = index
    #     end = len(events)
    #     while start < end:
    #         mid = start + (end - start) // 2

    def solve(events, index, k, dp):
        if index >= len(events) or k == 0:
            return 0
        if dp[index][k] != -1:
            return dp[index][k]
        aftertake = linearSearch(events, index) if linearSearch(events, index) else 0
        take = solve(events, aftertake, k - 1) + events[index][2]
        skip = solve(events, index + 1, k)
        dp[index][k] = max(take, skip)
        return dp[index][k]

    return solve(events, 0, k, dp)


def numBusesToDestination(routes, source, target):
    adj = {}
    if source == target:
        return 0
    for i in range(len(routes)):
        for j in range(len(routes[i])):
            if routes[i][j] in adj:
                adj[routes[i][j]].add(i)
            else:
                adj[routes[i][j]] = set()
    queue = deque()
    visited = set()
    for v in routes[source]:
        queue.append(v)
        visited.add(v)
    count = 1
    while queue:
        size = len(queue)
        while size:
            route = queue.popleft()
            for stop in route:
                if stop == target:
                    return count
                if stop in visited:
                    continue
                for nextroute in adj[stop]:
                    if nextroute in visited:
                        visited.add(nextroute)
                        queue.append(nextroute)
            size -= 1
        count += 1
    return -1


def slidingPuzzle(board):
    adj = {}
    start = ""
    for i in range(len(board)):
        for j in range(len(board[0])):
            start += str(board[i][j])
    adj[0] = {1, 3}
    adj[1] = {0, 2, 4}
    adj[2] = {1, 5}
    adj[3] = {0, 4}
    adj[4] = {1, 3, 5}
    adj[5] = {2, 4}
    visited = set()
    target = "123456"
    queue = deque()
    queue.append(start)
    steps = 0
    visited.add(start)

    def find(value):
        for i in range(len(value)):
            if value[i] == "0":
                return i

    while queue:
        size = len(queue)
        while size:
            value = queue.popleft()
            if value == target:
                return steps
            zero_index = find(value)
            for swapIdx in adj[zero_index]:
                state_list = list(value)
                state_list[zero_index], state_list[swapIdx] = (
                    state_list[swapIdx],
                    state_list[zero_index],
                )
                new_state = "".join(state_list)
                if new_state not in visited:
                    visited.add(new_state)
                    queue.append(new_state)
            size -= 1
        steps += 1
    return -1


def maxFreeTime(eventTime, startTime, endTime):
    freeArray = []
    freeArray.append(startTime[0])
    for i in range(1, len(startTime)):
        freeArray.append(startTime[i] - endTime[i - 1])

    maxRightFreeTime = [0] * len(startTime)
    for i in range(len(startTime) - 2, -1, -1):
        maxRightFreeTime[i] = max(maxRightFreeTime[i + 1], freeArray[i + 1])
    maxLeftFreeTime = [0] * len(startTime)
    for i in range(1, len(startTime)):
        maxLeftFreeTime[i] = max(maxLeftFreeTime[i + 1], freeArray[i - 1])

    result = 0
    for i in range(1, len(startTime)):
        currEvent = endTime[i - 1] - startTime[i - 1]
        if currEvent <= max(maxLeftFreeTime[i - 1], maxRightFreeTime[i]):
            result = max(result, freeArray[i - 1] + currEvent + freeArray[i])
        else:
            result = max(result, freeArray[i - 1] + freeArray[i])
    return result


def maxBalancedSubsequenceSum(nums):
    arr = []
    flag = True
    for i in range(len(nums)):
        if nums[i] >= 0:
            flag = False
        arr.append(nums[i] - i)
    if flag:
        return max(nums)
    dp = set()

    def solve(nums, arr, currIndex, prevIndex):
        if currIndex >= len(arr):
            return 0
        if (currIndex, prevIndex) in dp:
            return dp(currIndex, prevIndex)
        taken = float("inf")
        skip = float("inf")
        if prevIndex == -1 or arr[currIndex] >= arr[prevIndex]:
            taken = solve(nums, arr, currIndex + 1, currIndex) + nums[currIndex]
        skip = solve(nums, arr, currIndex + 1, prevIndex)
        dp[(currIndex, prevIndex)] = max(taken, skip)
        return dp[(currIndex, prevIndex)]

    return solve(nums, arr, 0, -1)


# print(maxBalancedSubsequenceSum([3, 3, 5, 6]))


# lis with patience sorting


def lower_bound(arr, target):
    left, right = 0, len(arr)

    while left < right:
        mid = (left + right) // 2
        if arr[mid] < target:
            left = mid + 1
        else:
            right = mid

    return left


def lis(arr):
    listArr = []
    listArr.append(arr[0])
    for i in range(1, len(arr)):
        if lower_bound(listArr, arr[i]):
            listArr[lower_bound(listArr, arr[i]) - 1] = arr[i]
        else:
            listArr.append(arr[i])
    return len(listArr)


def solve(currIndex, nums, result, temp, prev):
    if currIndex >= len(nums):
        if len(temp) > len(result):
            result = temp
        return

    if prev == -1 or nums[currIndex] % prev == 0:
        temp.append(nums[currIndex])
        solve(currIndex + 1, nums, result, temp, nums[currIndex])
        temp.pop()
    solve(currIndex, nums, result, temp, prev)


def largestDivisibleSubset(nums):
    nums.sort()
    # result = []
    # temp = []
    # prev = -1
    # solve(0, nums, result, temp, prev)
    # return result
    # bottoms up
    prev = [-1] * len(nums)
    dp = [1] * len(nums)
    last_chance_index = -1
    maxL = 1
    for i in range(len(nums)):
        for j in range(0, i):
            if nums[i] % nums[j] == 0:
                if dp[i] < dp[j + 1]:
                    dp[i] = dp[j] + 1
                    prev[i] = j

                if dp[i] > maxL:
                    maxL = dp[i]
                    last_chance_index = i
    result = []
    while last_chance_index != -1:
        result.append(nums[last_chance_index])
        last_chance_index = prev[last_chance_index]
    return result


def longestCommonSubsequence(str1, str2):
    dp = [[0 for _ in range(len(str1))] for _ in range(len(str2))]

    for i in range(len(str1)):
        for j in range(len(str2)):
            if str1[i - 1] == str2[j - 1]:
                dp[i][j] = 1 + dp[i - 1][j - 1]
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    result = ""
    k = len(str1)
    m = len(str2)
    while k > 0 and m > 0:
        if str1[k - 1] == str2[m - 1]:
            result.append(str1[k - 1])
            k -= 1
            m -= 1
        else:
            if dp[k - 1][m] > dp[k][m - 1]:
                k -= 1
            else:
                m -= 1
    return result.__reversed__()


def solves(s1, s2, m, n):
    if m == 0:
        return n
    elif n == 0:
        return m
    if s1[m - 1] == s2[n - 1]:
        return 1 + solves(s1, s2, m - 1, n - 1)
    else:
        return 1 + min(solves(s1, s2, m - 1, n), solves(s1, s2, m, n - 1))


def shortestSubseqcnes(s1, s2):
    return solves(s1, s2, len(s1), len(s2))


def minDistanceSolve(word1, word2, word1Index, word2Index, dp):
    if word1Index == len(word1):
        return len(word2) - word2Index
    if word2Index == len(word2):
        return len(word1) - word1Index
    if (word1Index, word2Index) in dp:
        return dp[(word1Index, word2Index)]
    delete = float("inf")
    replace = float("inf")
    insert = float("inf")
    if word1[word1Index] == word2[word2Index]:
        return minDistanceSolve(word1, word2, word1Index + 1, word2Index + 1, dp)
    if word1[word1Index] != word2[word2Index]:
        delete = minDistanceSolve(word1, word2, word1Index + 1, word2Index, dp) + 1
        insert = minDistanceSolve(word1, word2, word1Index, word2Index + 1, dp) + 1
        replace = minDistanceSolve(word1, word2, word1Index + 1, word2Index + 1, dp) + 1
    dp[(word1Index, word2Index)] = min(delete, replace, insert)
    return dp[(word1Index, word2Index)]


def minDistance(word1, word2):
    # dp = {}
    # return minDistanceSolve(word1, word2, 0, 0, dp)
    m, n = len(word1), len(word2)
    dp = [[0 for _ in range(n + 1)] for _ in range(m + 1)]
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
    for i in range(1, len(word1) + 1):
        for j in range(1, len(word2) + 1):
            if word1[i - 1] == word2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j], dp[i - 1][j - 1], dp[i][j - 1])
    return dp[len(word1)][len(word2)]


def check(s, index1, index2, dp):
    if index1 > index2:
        return True
    if dp[index1][index2] != -1:
        return dp[index1][index2]

    if s[index1] == s[index2]:
        dp[index1][index2] = check(s, index1 + 1, index2 - 1)
        return dp[index1][index2]
    dp[index1][index2] = False
    return dp[index1][index2]


def countSubstrings(s):
    n = len(s)
    count = 0
    dp = [[-1 for _ in range(len(s))] for _ in range(len(s))]
    for i in range(n):
        for j in range(1, n):
            if check(s, i, j, dp):
                count += 1
    return count


def countSubstringsBottomUp(s):
    dp = [[False for _ in range(len(s) + 1)] for _ in range(len(s) + 1)]
    count = 0
    for L in range(len(s) + 1):
        for i in range(i + L - 1):
            j = i + L - 1
            if i == j:
                dp[i][j] = True
            elif s[i] == s[j]:
                if L == 2:
                    dp[i][j] = True
                else:
                    dp[i][j] = dp[i + 1][j - 1]
            else:
                dp[i][j] = False
        if dp[i][j] == True:
            count += 1
    return count


def longestPalindrome(s):
    starting_point = 0
    maxlength = float("-inf")
    dp = {}

    def solve(s, i, j):
        if j >= i:
            return True
        if (i, j) in dp:
            return dp[(i, j)]
        if s[i] == s[j]:
            dp[(i, j)] = solve(s, i + 1, j - 1)
            return dp[(i, j)]
        dp[(i, j)] = False
        return dp[(i, j)]

    for i in range(len(s)):
        for j in range(1, len(s)):
            if solve(i, j) == True:
                if j - i + 1 > maxlength:
                    maxlength = j - i + 1
                    starting_point = i
    # return s[starting_point : maxlength + 1]
    dp_len = [[False for _ in range(len(s) + 1)] for _ in range(len(s) + 1)]
    for i in range(len(s)):
        for j in range(len(s)):
            if i == j:
                dp_len[i][j] = True

    for L in range(len(s)):
        for i in range(len(s) - L + 1):
            j = i + L - 1
            if s[i] == s[j] and L == 2:
                dp[i][j] = True
                maxlength = 2
                starting_point = i
            else:
                if s[i] == s[j] and dp[i + 1][j - 1] == True:
                    dp[i][j] = True
                    if j - i + 1 > maxlength:
                        maxlength = j - i + 1
                        starting_point = i
                else:
                    dp[i][j] = False
    return s[starting_point : maxlength + 1]


def minInsertions(s):
    dp = {}

    def minInsetionsSolve(s, i, j):
        if i >= j:
            return 0
        if (i, j) in dp:
            return dp[(i, j)]
        if s[i] == s[j]:
            dp[(i, j)] = minInsetionsSolve(s, i + 1, j - 1)
            return dp[(i, j)]
        else:
            dp[(i, j)] = 1 + min(
                minInsetionsSolve(s, i + 1, j), minInsetionsSolve(s, i, j - 1)
            )
            return dp[(i, j)]

    # return minInsetionsSolve(s, 0, len(s) - 1)
    dp_state = [[0 for _ in range(len(s) + 1)] for _ in range(len(s) + 1)]

    for L in range(len(s)):
        for i in range(len(s) - L + 1):
            j = i + L - 1
            if s[i] == s[j]:
                dp_state[i][j] = dp_state[i + 1][j - 1]
            else:
                dp_state[i][j] = 1 + min(dp_state[i + 1][j], dp_state[i][j - 1])
    return dp_state[len(s)][len(s)]


def partition(s):
    dp = [[0 for _ in range(len(s))] for _ in range(len(s))]
    count = 0
    for L in range(1, len(s) + 1):
        for i in range(len(s) + L - 1):
            j = i + L - 1
            if i == j:
                dp[i][j] = 1
            elif s[i] == s[j]:
                if L == 2:
                    dp[i][j] = 1
                else:
                    dp[i][j] = dp[i + 1][j - 1]
    result = []
    currPartiton = []

    def solve(i):
        if i == len(s):
            result.clear()
            result.extend(currPartiton)
            return
        for j in range(i, len(dp[0])):
            if dp[i][j] == 1:
                currPartiton.append(s[i : j + 1])
                solve(j + 1)
                currPartiton.pop()

    solve(0)
    return result


def maxOperations(nums):
    def solve(first, last, score):
        if last - first < 1:
            return 0
        first_two = 0
        first_last = 0
        last_Two = 0
        if score == 0 or score == nums[first] + nums[first + 1]:
            first_two = 1 + solve(first + 2, last, nums[first] + nums[first + 1])
        if score == 0 or score == nums[first] + nums[last]:
            first_last = 1 + solve(first + 1, last - 1, nums[first] + nums[last])
        if score == 0 or score == nums[last] + nums[last - 1]:
            last_Two = 1 + solve(first, last - 2, nums[last] + nums[last - 1])
        return max(first_two, first_last, last_Two)

    return solve(0, len(nums) - 1, 0)


def lengthOfLIS(nums):
    dp = {}

    def solve(index, prev):
        if index == len(nums):
            return 0
        if (index, prev) in dp:
            return dp[(index, prev)]
        skip = float("-inf")
        taken = float("-inf")
        skip = solve(index + 1, prev)
        if prev == -1 or nums[index] > prev:
            taken = 1 + solve(index + 1, nums[index])
        dp[(index, prev)] = max(taken, skip)
        return dp[(index, prev)]

    return solve(0, -1)


def minPathSum(grid):
    def solve(i, j):
        if i < 0 or i >= len(grid) or j < 0 or j >= len(grid[0]):
            return float("inf")
        if i == len(grid) - 1 and j == len(grid[0]) - 1:
            return grid[i][j]
        down = (
            solve(
                i + 1,
            )
            + grid[i][j]
        )
        right = solve(i, j + 1)
        return grid[i][j] + min(down, right)

    return solve(0, 0)


def findPaths(m, n, maxMove, startRow, startColumn):
    mod = pow(10, 9) + 7

    def solve(i, j):
        if i < 0 or i >= m or j < 0 or j >= n:
            return 1
        if maxMove == 0:
            return 0
        down = solve(i + 1, maxMove - 1)
        right = solve(i, j + 1, maxMove - 1)
        left = solve(i - 1, j, maxMove - 1)
        top = solve(i, j - 1, maxMove - 1)
        return (down + right + left + top) % mod

    return solve(startRow, startRow, maxMove)


def maxTotalReward(rewardValues):
    def solve(index, score):
        if index >= len(rewardValues):
            return 0
        skip = solve(index + 1, score)
        taken = 0
        if score == float("-inf") or rewardValues[index] > score:
            taken = solve(index + 1, score + rewardValues[index])
        return max(taken, skip)

    return solve(0, float("-inf"))


def uniquePaths(m, n):
    dp = [[0 for _ in range(n + 1)] for _ in range(m + 1)]
    for i in range(1, m):
        dp[i][0] = 1
    for i in range(1, n):
        dp[0][i] = 1

    for i in range(m):
        for j in range(n):
            dp[i][j] = dp[i - 1][j] + dp[i][j - 1]
    return dp[m - 1][n - 1]


def uniquePathsWithObstacles(obstacleGrid):
    dp = [
        [0 for _ in range(len(obstacleGrid[0]) + 1)]
        for _ in range(len(obstacleGrid) + 1)
    ]
    dp[0][0] = 1
    for i in range(1, len(obstacleGrid)):
        if obstacleGrid[i][0] == 0:
            dp[i][0] = 1
        else:
            return
    for i in range(1, len(obstacleGrid[0])):
        if obstacleGrid[0][i] == 0:
            dp[i][0] = 1
        else:
            return
    for i in range(1, len(obstacleGrid)):
        for j in range(1, len(obstacleGrid[0])):
            if obstacleGrid[i][j] == 0:
                dp[i][j] = dp[i - 1][j] + dp[i][j - 1]
    return dp[len(obstacleGrid) - 1][len(obstacleGrid[0]) - 1]


# def maximumLength(nums):
#     def solve(currIndex, previous, current_density, count):
#         if currIndex >= len(nums):
#             return 0
#         even = 0
#         odd=0
#         oddeven=0


#         return max(taken, skip)


#     return solve(0, oddEven)


# propagation sometimes form bottom right to top left
def solve(i, j, dungeon, dp):
    if i >= len(dungeon) or j >= len(dungeon[0]):
        return float("inf")
    if dp[i][j] != -1:
        return dp[i][j]

    if i == len(dungeon) - 1 and j == len(dungeon[0]) - 1:
        if dungeon[i][i] <= 0:
            return abs(dungeon[i][j]) + 1
        else:
            return 1
    right = solve(i, j + 1, dungeon)
    down = solve(i + 1, j, dungeon)
    result = min(right, down) - dungeon[i][j]
    dp[i][j] = 1 if result < 0 else result
    return dp[i][j]


def calculateMinimumHP(self, dungeon):
    # left = 1
    # right = 10**7 * 4
    # miniMumHealth = 10**7 * 4
    # m = len(dungeon)
    # n = len(dungeon[0])

    # def findCalculateMinimumHP(i, j, mid):
    #     if i >= m or j >= n:
    #         return False
    #     mid += dungeon[i][j]
    #     if mid <= 0:
    #         return False
    #     if i == m - 1 and j == n - 1:
    #         return True
    #     return findCalculateMinimumHP(i + 1, j, mid) or findCalculateMinimumHP(
    #         i, j + 1, mid
    #     )

    # while left <= right:
    #     mid = left + (right - left) // 2
    #     if findCalculateMinimumHP(0, 0, mid) >= 0:
    #         miniMumHealth = min(miniMumHealth, mid)
    #         right = mid - 1
    #     else:
    #         left = mid + 1
    # return miniMumHealth

    # dp = [[-1 for _ in range(201)] for _ in range(201)]

    # def solve(i, j, dungeon, dp):
    #     if i >= len(dungeon) or j >= len(dungeon[0]):
    #         return float("inf")
    #     if dp[i][j] != -1:
    #         return dp[i][j]

    #     if i == len(dungeon) - 1 and j == len(dungeon[0]) - 1:
    #         if dungeon[i][i] <= 0:
    #             return abs(dungeon[i][j]) + 1
    #         else:
    #             return 1
    #     right = solve(i, j + 1, dungeon)
    #     down = solve(i + 1, j, dungeon)
    #     result = min(right, down) - dungeon[i][j]
    #     dp[i][j] = 1 if result < 0 else result
    #     return dp[i][j]

    # return solve(0, 0, dungeon, dp)
    m = len(dungeon)
    n = len(dungeon[0])
    dp = [[0 for _ in range(201)] for _ in range(201)]
    dp[m][n - 1] = dp[m - 1][n] = float("inf")

    for i in range(m - 1, -1, -1):
        for j in range(n - 1, -1, -1):
            if i == m - 1 and j == n - 1:
                if dungeon[i][j] <= 0:
                    dp[m - 1][n - 1] = abs(dungeon[m - 1][n - 1]) + 1
                else:
                    dp[m - 1][n - 1] = 1
            right = dp[i + 1][j]
            down = dp[i][j + 1]
            result = min(right, down) - dungeon[i][j]
            dp[i][j] = 1 if result < 0 else result
    return dp[0][0]


def maximumLength(nums):
    def solve(currIndex, previous, current_score):
        if currIndex >= len(nums):
            return 0
        taken = 0
        if previous == -1 or (nums[currIndex] + previous) % 2 == current_score:
            if currIndex >= len(nums) - 2:
                if (nums[currIndex] + nums[currIndex]) % 2 == current_score:
                    return 2
                else:
                    return 0
            else:
                taken = 1 + solve(
                    currIndex + 1, nums[currIndex + 1], (nums[currIndex] + previous) % 2
                )
        skip = solve(currIndex + 1, previous, current_score)
        return max(taken, skip)

    return solve(0, -1, 0)


def maxSum(nums):
    st = set()
    sums = 0
    maxNeg = float("-inf")

    for num in nums:
        if num <= 0:
            maxNeg = max(maxNeg, num)
        elif num not in st:
            sums += num
            st.add(num)
    return maxNeg if sums == 0 else sums


print(maxSum([1, 2, 3, 4, 5]))
