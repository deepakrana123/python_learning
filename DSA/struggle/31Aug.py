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
