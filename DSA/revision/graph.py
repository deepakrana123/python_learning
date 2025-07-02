#  i wants to kill this thinks
from collections import deque
import heapq
from ordered_set import OrderedSet


class GraphSolution:
    def dfs(self, adj, currNode, visited):
        if visited[currNode]:
            return
        visited[currNode] = True
        self.result.append(visited)
        for node in adj[currNode]:
            if visited[currNode] is False:
                self.dfs(adj, node, visited)

    def solve(self, nodes):
        adj = {}
        for u, v in nodes:
            if u not in adj:
                adj[u] = set()
            if v not in adj:
                adj[v] = set()
            adj[u].append(v)
            adj[v].append(u)
        self.result = []
        self.stack = []
        visited = [False] * len(nodes)
        self.dfs(adj, 0, visited)
        return self.result

    def bfs(self, adj, currNode, visited):
        queue = deque([])
        queue.append(currNode)
        visited[currNode] = True
        self.append(currNode)
        while queue:
            u = queue.popleft()
            for node in adj[u]:
                if visited[node] == False:
                    queue.append(node)
                    visited[node] = True
                    self.result.append(node)

    def undirectedDfsCycle(self, adj, currNode, parentNode, visited):
        if visited[currNode] == True:
            return False
        visited[currNode] = True
        for node in adj[currNode]:
            if node == parentNode:
                continue
            # if visited[node] == True:
            #     return True
            if visited[node] == True or self.undirectedDfsCycle(
                adj, node, currNode, visited
            ):
                return True
        return False

    # chances are there there will be do graphs to so loop on them also , or two components one
    def undirectedBfsCycle(self, adj, currNode, parentNode, visited):
        queue = deque([])
        if visited[currNode] == True:
            return True
        queue.append([currNode, parentNode])
        while queue:
            node, parent = queue.popleft()
            for nodes in adj[node]:
                if nodes == parent:
                    continue
                if visited[nodes] == True and nodes != parent:
                    return True
                if visited[nodes] == False:
                    queue.append([nodes, node])

    def dfsdirectedCycle(self, adj, currNode, visited):
        if visited[currNode]:
            return
        visited[currNode] = True
        for node in adj[currNode]:
            if visited[currNode] is False:
                self.dfs(adj, node, visited)
        self.stack.append(currNode)

    def toposortWithBfs(self, adj):
        indegree = [0] * len(adj)
        for u in range(len(adj)):
            for v in adj[u]:
                indegree[v] += 1

        queue = deque([])
        for i in range(len(indegree)):
            if indegree[i] == 0:
                queue.append(i)

        sortedTopo = []
        while queue:
            node = queue.appendleft()
            sortedTopo.append(node)
            for currNode in adj[node]:
                indegree[currNode] -= 1
                if indegree[currNode] == 0:
                    queue.append(currNode)
        return {sortedTopo, indegree}

    def cycleinDirectedBfs(self, adj):
        results, indegree = self.toposortWithBfs(adj)
        for i in range(len(indegree)):
            if indegree[i] != 0:
                return False
        return True

    def cycleinDirectedBfsOtherLogic(self, adj):
        indegree = [0] * len(adj)
        for u in range(len(adj)):
            for v in adj[u]:
                indegree[v] += 1
        queue = deque([])
        for i in range(len(indegree)):
            if indegree[i] == 0:
                queue.append(i)
        count = 0
        sortedTopo = []
        while queue:
            count += 1
            node = queue.appendleft()
            sortedTopo.append(node)
            for currNode in adj[node]:
                indegree[currNode] -= 1
                if indegree[currNode] == 0:
                    queue.append(currNode)
        return count == len(adj)

    # is birpartite

    def isbipartite(self, adj, currColor, currColorStack, currNode):
        currColorStack[currNode] = currColor

        for node in adj[currNode]:
            if currColorStack[node] == currColor:
                return False
            if self.isbipartite(adj, 1 - currColor, currColorStack, currNode) == False:
                return False
        return True

    def isbipartiteWithBds(self, adj, currColor, currColorStack, currNode):
        queue = deque([])
        queue.append(currNode)
        currColorStack[currNode] = currColor
        # self.append(currNode)
        while queue:
            u = queue.popleft()
            for node in adj[u]:
                if currColorStack[node] == currColor:
                    return False
                if currColorStack[node] == -1:
                    currColorStack[node] = 1 - currColorStack[u]
                    queue.append(node)
        return True

    def find(self, currNode, parentVecotr):
        if currNode == parentVecotr[currNode]:
            return
        return self.find(parentVecotr[currNode], parentVecotr)

    # def dsu(self, adj):
    #     pass
    def dejistrka(self, adj, soucre):
        heap = []
        result = [float("inf")] * len(adj)
        result[soucre] = 0
        heapq.heappush(heap, (0, soucre))
        while heap:
            currDistance, node = heapq.heappop(heap)
            for temp in adj[node]:
                distance, currNode = temp
                if currDistance + distance < result[currNode]:
                    result[currNode] = currDistance + distance
                    heapq.heappush(heap, (currDistance + distance, currNode))
        return result

    def dejistrkaSet(self, adj, source):
        heap = []
        result = [float("inf")] * len(adj)
        result[source] = 0
        order_set = OrderedSet()
        order_set.add((0, source))
        while heap:
            currDistance, node = next(iter(order_set))
            order_set.discard(currDistance)
            for temp in adj[node]:
                distance, currNode = temp
                if currDistance + distance < result[currNode]:
                    if result[currNode] != float("inf"):
                        old_entry = (result[currNode], currNode)
                        if old_entry in order_set:
                            order_set.discard(old_entry)
                        result[currNode] = currDistance + distance
                        order_set.add((currDistance + distance, currNode))
        return result
