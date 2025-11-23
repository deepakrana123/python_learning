import heapq
from collections import deque


def maxEvents(self, events):
    events.sort(key=lambda e: e[0])
    heap = []
    days = events[0][0]
    i = 0
    count = 0
    while heap or i < len(events):
        if heap:
            days = max(days, events[i][0])
        while events[i][0] == days:
            heapq.heappush(heap, events[i][1])
            i += 1
        if heap:
            heapq.heappop(heap)
            count += 1
            days += 1
        while heap and heap[-1] < days:
            heapq.heappop(heap)
    return count


from collections import defaultdict


class Graph:

    def __init__(self, n: int, edges):
        self.adj = defaultdict(list)
        self.N = n
        self.heap = []
        for u, v, w in edges:
            self.adj[u].append((v, w))

    def addEdge(self, edge):
        u, v, w = edge
        self.adj[u].append((v, w))

    def shortestPath(self, node1: int, node2: int):
        result = [float("inf")] * self.N
        result[node1] = 0
        heapq.heappush(self.heap, (0, node1))
        while self.heap:
            currDistance, node = heapq.heappop(self.heap)
            if node == node2:  # early stopping
                return currDistance
            if currDistance > result[node]:
                continue
            for temp in self.adj[node]:
                distance, currNode = temp
                if currDistance + distance < result[currNode]:
                    result[currNode] = currDistance + distance
                    heapq.heappush(self.heap, (currDistance + distance, currNode))
        return -1 if result[node2] == float("inf") else result[node2]


class Solution1:
    def __init__(self):
        self.dirs = [[-1, 0], [0, 1], [1, 0], [0, -1]]

    def minimumObstacles(self, grid):
        # result = [float("inf")]
        # m, n = len(grid), len(grid[0])
        # visited = [[False] * n for _ in range(m)]
        # dq = deque()
        # dq.append((0, 0, 0))  # (x, y, steps)
        # visited[0][0] = True

        # while dq:
        #     x, y, steps = dq.popleft()
        #     if x == m - 1 and y == n - 1:
        #         return steps  # shortest path

        #     for dx, dy in self.dirs:
        #         nx, ny = x + dx, y + dy
        #         if 0 <= nx < m and 0 <= ny < n and not visited[nx][ny]:
        #             visited[nx][ny] = True
        #             dq.append((nx, ny, steps + 1))

        # return -1
        heap = []
        heapq.heappush(heap, (0, (0, 0)))
        result = [[float("inf") for _ in range(len(grid[0]))] for _ in range(len(grid))]
        result[0][0] = 0
        while heap:
            wegiht, index = heapq.heappop(heap)
            currI, currJ = index
            for d in self.dirs:
                dI, dJ = d
                _currI = currI + dI
                _currJ = currJ + dJ
                if (
                    _currI < 0
                    and _currI >= len(grid)
                    and _currJ < 0
                    and _currJ >= len(grid[0])
                ):
                    continue
                wt = 1 if (grid[_currI][_currJ] == 1) else 0
                if wegiht + wt < result[_currI][_currJ]:
                    result[_currI][_currJ] = wegiht + wt
                    heapq.heappush(heap, (wegiht + wt, (_currI, _currJ)))
        return result[len(grid) - 1][len(grid[0]) - 1]
    
    def slidingPuzzle(self, board):
        
