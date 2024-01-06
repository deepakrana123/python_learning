class Graph:
    def __init__(self,n:int,edges:List[List[int]]):
        self.graph=[[float("inf")]*n for _ in range(n)]
        for edge in edges:
            u=edge[0]
            v=edge[1]
            weight=edge[2]
            self.graph[u][v]=weight
        for i in range(len(self.graph)):
            self.graph[i][i]=0
        n=len(self.graph)
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    self.graph[i][j]=min(self.graph[i][k]+self.graph[k][j],self.graph[i][j])

    # def __init__(self, n: int, edges: List[List[int]]):
    #     self.graph={i:[] for i in range(n)}
    #     for edge in edges:
    #         u=edge[0]
    #         v=edge[1]
    #         weight=edge[2]
    #         self.graph[u].append((v,weight))
    def addEdge(self, edge: List[int]) -> None:
         u=edge[0]
         v=edge[1]
         weight=edge[2]
         for i in range(len(self.graph)):
             for j in range(len(self.graph)):
                 self.graph[i][j]=min(self.graph[i][j],self.graph[i][u]+weight+self.graph[v][j])
    def shortestPath(self, node1: int, node2: int) -> int:
        # return self.graph[node1][node2]
        return -1 if self.graph[node1][node2] == float('inf') else self.graph[node1][node2]

    # def dijistra(self,node1,node2):
    #     distances = {node: float('inf') for node in self.graph}
    #     distances[node1] = 0
    #     priority_queue = [(0, node1)]
    #     while priority_queue:
    #         current_distance, current_node = heapq.heappop(priority_queue)
    #         if current_distance > distances[current_node]:
    #             continue
    #         for edge in self.graph[current_node]:
    #             v,vDistance=edge
    #             distance = current_distance + vDistance
    #             if distance < distances[v]:
    #                 distances[v] = distance
    #                 heapq.heappush(priority_queue, (distance, v))
    #     return -1 if distances[node2] == float('inf') else distances[node2]

    
        


# Your Graph object will be instantiated and called as such:
# obj = Graph(n, edges)
# obj.addEdge(edge)
# param_2 = obj.shortestPath(node1,node2)