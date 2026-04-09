def triangleType(nums):
    a, b, c = nums
    if a == b == c:
        return "equilateral"
    elif (a == b and b != c) or (b == c and a != b):
        return "isosceles"
    elif a != b and b != c and a != c:
        return "scalene"
    else:
        "none"


def isZeroArray(nums, queries):
    result = nums
    n = len(nums)
    for i in range(len(queries)):
        start = queries[i][0]
        end = queries[i][1] + 1
        result[start] += 1
        if end < n:
            result[end] -= 1
    cumSum = 0
    diff = [0] * n
    for i in range(n):
        cumSum += result[i]
        diff[i] = cumSum
    for i in range(n):
        if result[i] < nums[i]:
            return False
    return True


def getLongestSubsequence(words, groups):
    n = len(words)
    result = []
    for i in range(1, n + 1):
        if groups[i] != groups[i - 1]:
            result.append(words[i])
    return result


from collections import deque


def bfs(start, adj, k, n):
    queue = deque()
    queue.append((start, 0))
    visitor = [False] * n
    visitor[start] = True
    count = 0
    while queue:
        curr, dist = queue.pop()
        if dist > k:
            continue
        count += 1
        for nigb in adj[curr]:
            if not visitor[nigb]:
                visitor[nigb] = True
                queue.append((nigb, dist + 1))
    return count


def dfs(start, adj, k, n, currParent):
    if k < 0:
        return
    count = 1
    for nigb in adj[start]:
        if nigb != currParent:
            count += dfs(nigb, adj, k - 1, n, start)
    return count


def findCount(edge, k):
    n = len(edge) + 1
    adj = {}
    for e in edge:
        u, v = e
        adj[u].append(v)
        adj[v].append(u)
    result = [bfs(i, adj, k, n) for i in range(n)]
    return result


def maxTargetNodes(edges1, edges2, k):
    if k == 0:
        return [1] * len(edges1) + 1
    result1 = findCount(edges1, k)
    result2 = findCount(edges2, k - 1)
    maxLargeNodeCount = max(result2)
    result1 = [maxLargeNodeCount + result1[i] for i in range(len(edges1))]
    return result1
