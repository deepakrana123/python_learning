def mostProfitablePath(edges, bob, amount):
    n = len(amount)
    aliceIncome = float("-inf")
    adj = {i: [] for i in range(n)}
    bobVsited = [False] * n
    bobMap = {}

    def dfs(adj, bob, time, bobVisited):
        bobVsited[bob] = True
        bobMap[bob] = time
        if bob == 0:
            return True
        for negi in adj[bob]:
            if bobVisited[negi] == False:
                if dfs(adj, negi, time + 1, bobVisited):
                    return True
        del bobMap[bob]
        return False

    aliceVisited = [False] * n

    def dfsAlice(adj, time, income, aliceVsited, curr):
        aliceVisited[curr] = True
        if curr not in bobMap or time < bobMap[curr]:
            income += amount[curr]
        elif time == bobMap[curr]:
            income += amount[curr] // 2
        if len(adj[curr]) == 1:
            aliceIncome = max(income, aliceIncome)
        for edge in adj[curr]:
            if aliceVisited[edge] == False:
                dfsAlice(adj, time + 1, income, aliceVsited, edge)

    for edge in edges:
        u = edge[0]
        v = edge[1]
        adj[u].append(v)
        adj[v].append(u)
    dfs(adj, bob, 0)
    dfs(adj, 0, 0, aliceVisited, 0)
    return aliceIncome


def numOfSubarrays(arr):
    prefix = arr[0]
    count = 0
    odd = 0
    even = 0
    for i in range(1, len(arr)):
        prefix[i] = prefix[i] + prefix[i - 1]
    for i in range(len(arr)):
        if prefix[i] % 2 == 0:
            count += (count + odd) % (pow(10, 7) + 9)
            even += 1
        else:
            count += (count + even) % (pow(10, 7) + 9)
            odd += 1
    return count


print(numOfSubarrays([2, 2, 5, 6, 2]))


def maxAbsoluteSum(arr):
    max_current = max_global = arr[0]
    min_current = min_global = arr[0]

    for i in range(1, len(arr)):
        max_current = max(arr[i], max_current + arr[i])
        if max_current > max_global:
            max_global = max_current
    for i in range(1, len(arr)):
        min_current = min(arr[i], min_current + arr[i])
        if min_current < min_global:
            min_global = min_current
    return max(abs(min_global), abs(max_global))


print(maxAbsoluteSum([2, -5, 1, -4, 3, -2]))
print(maxAbsoluteSum([1, -3, 2, 3, -4]))
