class Solution:
    # def find(self, x):
    #     if self.parent[x] != x:
    #         self.parent[x] = self.find(self.parent[x])
    #     return self.parent[x]

    # def union(self, x, y):
    #     root_x = self.find(x)
    #     root_y = self.find(y)
    #     if root_x != root_y:
    #         if self.rank[root_x] < self.rank[root_y]:
    #             self.parent[root_x] = root_y
    #         elif self.rank[root_x] < self.rank[root_y]:
    #             self.parent[root_y] = root_x
    #         else:
    #             self.parent[root_y] = root_x
    #             self.rank[root_x] += 1
    #     else:
    #         return True
    #     return False

    # def makeConnected(self, n, connections):
    #     self.parent = [i for i in range(n)]
    #     self.rank = [0] * n
    #     extraEdges = 0
    #     components = n
    #     for u, v in connections:
    #         if not self.union(u, v):
    #             extraEdges += 1
    #         else:
    #             components -= 1
    #     return components - 1 if extraEdges >= components - 1 else -1
    def dfs(self, graph, i, visited):
        visited.add(i)
        for value in graph[i]:
            if value not in visited:
                visited.add(value)
                self.dfs(graph, value, visited)

    def makeConnected(self, n, connections):
        if len(connections) < n - 1:
            return -1
        graph = {i: [] for i in range(n)}
        for u, v in connections:
            graph[u].append(v)
            graph[v].append(u)
        visited = set()
        component = n
        for i in range(n):
            if i not in visited:
                component -= 1
                self.dfs(graph, i, visited)
        return component - 1


def giveIndex(days, index, duration):
    value = days[index] + duration
    for i in range(len(days)):
        if days[i] >= value:
            return i
    return len(days)


def mincostTickets(days, costs):
    dp = [0] * (len(days) + 1)
    dp[len(days) + 1] = 0

    # def solve(index):
    #     if index >= len(days):
    #         return 0
    #     if dp[index] != -1:
    #         return dp[index]
    #     min1st = costs[0] + solve(index + 1)
    #     min7st = costs[1] + solve(index + giveIndex(days, index, 7) + 1)
    #     min30st = costs[2] + solve(index + giveIndex(days, index, 30) + 1)
    #     dp[index] = min(min1st, min7st, min30st)
    #     return dp[index]

    # return solve(0)
    n = len(days)
    for i in range(len(days), -1, -1):
        min1st = costs[0] + dp[i + 1]
        j = i
        while j < n and days[j] < days[i] + 7:
            j += 1
        min7st = costs[1] + dp[j]

        k = i
        while k < n and days[k] < days[i] + 30:
            k += 1
        min30th = costs[2] + dp[k]
        dp[i] = min(min1st, min30th, min7st)
    return dp[0]


def smallestSubarrays(nums):
    bitSet = [-1] * 32
    result = [0] * len(nums)
    for i in range(len(nums) - 1, -1, -1):
        endIndex = i
        for j in range(32):
            if not nums[i] & 1 << j:
                if bitSet[j] != -1:
                    endIndex = max(endIndex, bitSet[j])
                else:
                    bitSet[j] = i
        result[i] = endIndex - i + 1
    return result


# Definition for a Node.
class Node:
    def __init__(self, val=0, neighbors=None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []


class Solutions:
    def dfs(self, node, clone_node):
        for neigh in node.neighbors:
            if neigh not in self.mp:
                new_clone_node = Node(neigh.val)
                self.mp[neigh] = new_clone_node
                clone_node.neighbors.append(new_clone_node)
                self.dfs(neigh, new_clone_node)
            else:
                clone_node.neighbors.append(self.mp[neigh])

    def cloneGraph(self, node):
        self.mp = {}
        clone_node = Node(node.val)
        self.mp[node] = clone_node
        self.dfs(node, clone_node)
        return clone_node


def removeDuplicateLetters(s):
    stack = []
    dicts = {}
    seen = set()
    for i in range(len(s)):
        dicts[s[i]] = i

    for i in range(len(s)):
        if s[i] in seen:
            continue
        if stack and s[i] < stack[-1] and dicts[s[i]] > i:
            stack.pop()
            seen.remove(stack[-1])
        else:
            stack.append(s[i])
            seen.add(stack[-1])
    return "".join(stack)


def removeKdigits(num, k):
    stack = []
    i = 0
    while i < len(num):
        if stack and k > 0 and stack[-1] > num[i]:
            stack.pop()
            k -= 1
        stack.append(num[i])
        i += 1

    while k > 0:
        stack.pop()
        k -= 1
    return "".join(stack).lstrip("0") if len("".join(stack).lstrip("0")) != 0 else 0


def dailyTemperatures(temperatures):
    stack = []
    answer = []
    for i in range(len(temperatures) - 1, -1, -1):
        while stack and temperatures[stack[-1]] <= temperatures[i]:
            stack.pop()
        if stack:
            answer[i] = stack[-1] - i
        stack.append(i)
    return answer


def minWindow(s, t):
    left = 0
    right = 0
    temp_count = {}
    check_count = {}

    for ch in t:
        check_count[ch] = check_count.get(ch, 0) + 1
    have, need = 0, len(check_count)
    res = [0, 0]
    res_len = float("inf")
    while right < len(s):
        ch = s[right]
        temp_count[ch] = temp_count.get(ch, 0) + 1
        if ch in check_count and temp_count[ch] == check_count[ch]:
            have += 1
        while have == need:
            res = [left, right]
            res_len = min(res_len, right - left + 1)
            temp_count[s[left]] -= 1
            if s[left] in check_count and temp_count[s[left]] < check_count[s[left]]:
                have -= 1
        right += 1
    l, r = res
    return s[l : r + 1] if res_len != float("inf") else ""


def longestSubarray(nums):
    maxValue = nums[0]
    count = 1
    result = float("-inf")
    for i in range(1, len(nums)):
        print(maxValue, nums[i], i)
        if nums[i] == maxValue:
            count += 1
            result = max(result, count)
        else:
            maxValue = nums[i]
            count = 1
    return result


def singleNumber(nums):
    # a = nums[0]
    # for i in range(1, len(nums)):
    #     a ^= nums[i]
    # return a
    result = 0
    for i in range(32):
        bit_sum = 0
        for num in nums:
            bit_sum += num >> i
        result |= (bit_sum % 3) << i


from collections import defaultdict


# def findCheapestPrice(n, flights, src, dst, k):
#     heap = [(0, src, k + 1)]
#     adj = defaultdict(list)
#     for u, v, w in flights:
#         adj[u].append((v, w))

#     while heap:
#         current_dist, node, stops = heapq.heappop(heap)
#         if node == dst:
#             return current_dist
#         if stops > 0:
#             for v, weight in adj[node]:
#                 heapq.heappush(heap, (current_dist + weight, v, stops - 1))

#     return -1


# def addOperators(num, target):
#     def solve(index, prev_value, curr_value):
#         if index >= len(num):
#             if curr_value == target:
#                 return 1
#             else:
#                 return 0

#         solve(index + 1, num[index], prev_value + num[index])
#         solve(index, num[index], prev_value - num[index])

#         solve(index + 1, num[index], prev_value - num[index])
#         solve(index, num[index], prev_value + num[index])

#         solve(index + 1, num[index], prev_value * num[index])
#         solve(index, num[index], prev_value / num[index])

#     return solve(0, num[0], num[0])


def minCost(basket1, basket2):
    dicts = {}
    min_element = float("inf")
    for v in basket1:
        dicts[v] = dicts.get(v, 0) + 1
        min_element = min(min_element, v)
    for v in basket2:
        dicts[v] = dicts.get(v, 0) - 1
        min_element = min(min_element, v)
    finalList = []
    for v in dicts:
        if dicts[v] == 0:
            continue

        if dicts[v] % 2 != 0:
            return -1

        for _ in range(1, dicts[v] // 2 + 1):
            finalList.append(v)
    finalList.sort()
    result = 0
    for i in range(len(finalList) // 2):
        result += min(finalList[i], min_element * 2)
    return result


def minCost(n, cuts):
    cuts.append(n)
    cuts.insert(0, 0)
    cuts.sort()

    def solve(i, j, cuts):
        if i > j:
            return 0

        mini = float("inf")
        for ind in range(i, j + 1):
            cost = (
                cuts[j + 1]
                - cuts[i - 1]
                + solve(i, ind - 1, cuts)
                + solve(ind + 1, j, cuts)
            )
            mini = min(cost, mini)
        return mini

    return solve(1, len(cuts) - 2, cuts)


def productQueries(n, queries):
    binary = format(n, "b")[::-1]
    arr = [1]
    mod = pow(10, 9) + 7
    for i in range(len(binary)):
        if binary[i] == "1":
            arr.append(arr[-1] * (2**i) % mod)
    result = []
    for i in range(len(queries)):
        l, r = arr[queries[i][0]], arr[queries[i][1] + 1]
        ans = r * pow(l, mod - 2, mod) % mod
        result.append(ans)

    return result


def reorderedPowerOf2(n):
    a = set()
    for i in range(31):
        abc = "".join(sorted(str(2**i), reverse=True))
        a.add(abc)
    return "".join(sorted(n)) in a


def countSquares(matrix):
    mat = [[0 for _ in range(len(matrix[0]))] for _ in range(len(matrix))]
    for i in range(len(matrix[0])):
        mat[0][i] = matrix[0][i]
    for i in range(len(matrix)):
        mat[i][0] = matrix[i][0]

    for i in range(1, len(matrix)):
        for j in range(1, len(matrix[0])):
            mat[i][j] = matrix[i][j] + min(
                mat[i - 1][j], mat[i - 1][j - 1], mat[i][j - 1]
            )
    results = 0
    for i in range(len(mat)):
        for j in range(len(mat[0])):
            results += mat[i][j]
    return results


def sumOfGoodSubsequences(nums):
    results = 0

    # def solve(curr, prev_value):
    #     if curr >= len(nums):
    #         return 0
    #     skip = solve(curr + 1, prev_value)
    #     taken = 0
    #     # print(curr, prev_value)
    #     if prev_value == -1 or abs(nums[curr] - prev_value) == 1:
    #         taken = nums[curr] + solve(curr + 1, nums[curr])
    #         print(f"Taking {nums[curr]} at index {curr}, total {taken + skip}")
    #     return taken + skip

    # # for i in range(len(nums)):
    # results += solve(0, -1)
    # return results
    def solve(curr, prev_value):
        if curr >= len(nums):
            return 0
        # skip current index
        # skip = solve(curr + 1, prev_value)
        taken = solve(curr + 1, prev_value)
        # take current index if starting new subsequence or consecutive
        if prev_value == -1 or abs(nums[curr] - prev_value) == 1:
            taken = nums[curr] + solve(curr + 1, nums[curr])
        return taken

    return solve(0, -1)


def minimumSum(grid):
    maxRow1 = -1
    maxCol1 = -1
    minRow1 = float("inf")
    minCol1 = float("inf")
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == 1:
                maxCol1 = max(maxCol1, j)
                minCol1 = min(minCol1, j)
                maxRow1 = max(maxRow1, i)
                minRow1 = min(minRow1, i)

    return (maxCol1 - minCol1 + 1) * (maxRow1 - minRow1 + 1)


from collections import defaultdict


def numberOfArithmeticSlices(nums):
    dicts = defaultdict(dict)
    mp = [{} for _ in range(len(nums))]
    result = 0
    for i in range(len(nums)):
        for j in range(0, i):
            diff = nums[j] - nums[i]
            # if diff not in mp[i]:
            #     mp[j][diff] += 1
            # else:
            #     mp[j][diff] = 1
            count_at_j = mp[j][diff][1] if mp[j][diff] else 0
            mp[i][diff] = mp[i].get(diff, 0) + 1
            result += count_at_j
    return result
