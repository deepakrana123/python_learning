import heapq
from typing import List
class Solution:
    def dijkstra(self,edges,n,source,destination):
        graph={i:[] for i in range(n)}
        for edge1,edge2,edge3 in edges:
            if edge3!=-1:
                graph[edge1].append((edge2,edge3))
                graph[edge2].append((edge1,edge3))
        distances = {node: float('inf') for node in graph}
        visited=[False]*n
        distances[source] = 0
        priority_queue = [(0, source)]
        while priority_queue:
            current_distance, current_node = heapq.heappop(priority_queue)
            if visited[current_node]==True:
                continue
            visited[current_node]=True
            for neighbor, weight in graph[current_node]:
                distance = current_distance + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    heapq.heappush(priority_queue, (distance, neighbor))
        return distances[destination]
            
    def modifiedGraphEdges(self, n: int, edges: List[List[int]], source: int, destination: int, target: int) -> List[List[int]]:
        currentShortestDistance=self.dijkstra(edges,n,source,destination)
        if currentShortestDistance < target:
            return []
        matchedTarget = currentShortestDistance == target
        for i in range(len(edges)):
            if edges[i][2] == -1:
                print(edges[i],matchedTarget)
                edges[i][2] = float("inf") if matchedTarget==True else 1
                if  matchedTarget==False:
                    newShortestDistance = self.dijkstra(edges, n, source, destination)
                    print(newShortestDistance)
                    if newShortestDistance < target:
                        edges[i][2] += (target - newShortestDistance)
                        matchedTarget = True
                
        final_distance = self.dijkstra(edges, n, source, destination)
        if final_distance != target:
            return []
        return edges
        
a=Solution()
print(a.modifiedGraphEdges(5,[[1,4,1],[2,4,-1],[3,0,2],[0,4,-1],[1,3,10],[1,0,10]],0,2,15))
        