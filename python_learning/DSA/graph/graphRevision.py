#graph representation
# adjancey matrix and adjancey list


# class Solution:
#     # def dfs(visited,trust,currNode):
#     #     visited[currNode]=True
#     #     for u,v in
#     def findJudge(self, n: int, trust) -> int:
#         self.result=-1
#         self.graph={i:[] for i in range(1,n+1)}
#         for u,v in trust:
#             self.graph[u].append(v)
#         for item in self.graph:
#             if(len(self.graph[item])==0):
#                 self.result=item
        
#         for item in self.graph:
#             if self.result not in  self.graph[item] and self.result!=item:
#                 return -1
#         return self.result
# a=Solution()
# print(a.findJudge(3,[[1,3],[2,3]]))
from collections import deque
class Solution:
    # def bfs(self,adj,curr,visited):
    #     visited[curr]=True
    #     queue=deque()
    #     queue.append(curr)
    #     while queue:
    #         currIndex=queue.popleft()
    #         for v in adj[currIndex]:
    #             if visited[v]==False:
    #                 self.bfs(adj,v,visited)
    def dfs(self,adj,curr,visited):
        visited[curr]=True
        for v in adj[curr]:
            if visited[v]==False:
                self.dfs(adj,v,visited)
    def findCircleNum(self, isConnected) -> int:
        adj={i:[] for i in range(len(isConnected))}
        for i in range(len(isConnected)):
            for j in range(len(isConnected[0])):
                if isConnected[i][j]==1:
                    adj[i].append(j)
                    adj[j].append(i)
        visited=[False]*len(isConnected)
        count=0
        for i in range(len(isConnected)):
            if visited[i]==False:
                self.dfs(adj,i,visited)
                count+=1
        return count
a=Solution()
print(a.findCircleNum([[1,1,0],[1,1,0],[0,0,1]]))


class newSolution:
    def dfs(self,adj,curr,visited):
        visited[curr]=True
        for v in adj[curr]:
            if visited[v]==False:
                self.dfs(adj,v,visited)
    def numberOfConnected(self,isConnect,n):
        adj={i:[] for i in range(n)}
        for i in range(len(isConnect)):
            u,v=isConnect[i]
            adj[v].append(u)
            adj[u].append(v)
        visited=[False]*n
        count=0
        for i in range(n):
            if visited[i]==False:
                self.dfs(adj,i,visited)
                count+=1
        return count
a=newSolution()
print(a.numberOfConnected([[0, 1], [1, 2], [2, 3], [3, 4]],5))


class isTreeGraph:
    def dfs(self,adj,curr,visited):
        visited[curr]=True
        for v in adj[curr]:
            if visited[v]==False:
                self.dfs(adj,v,visited)
    def CheckCycle(self,adj,visited,curr,parent):
        visited[curr]=True
        for v in adj[curr]:
            if v==parent:
                continue
            if visited[v]==True:
                continue
            if self.CheckCycle(adj,visited,v,curr)==False:
                return False
        return True

            
    def isTreeGarph(self,n,edges):
        adj={i:[] for i in range(n)}
        for i in range(len(edges)):
            u,v=edges[i]
            adj[v].append(u)
            adj[u].append(v)
        visited=[False]*n
        for i in range(n):
            if visited[i]==False:
                self.dfs(adj,i,visited)
        for value in visited:
            if value==False:
                return "Not Connected"
        visited=[False]*n
        return self.CheckCycle(adj,visited,0,-1)
        
a=isTreeGraph()
# print(a.isTreeGarph(n = 5, edges = [[0,1], [1,2], [2,3], [1,3], [1,4]]))

class isBipartite:
    def checkbipartite(self,adj,curr,color,currColor):
        color[curr]=currColor
        for v in adj[curr]:
            if color[v]==color[curr]:
                return False
            if color[v] == -1:
                colorOfV=1-currColor
                if self.checkbipartite(adj,v,color,colorOfV)==False:
                    return False
        return True
    def isBipartite(self, graph):
        adj={i:[] for i in range(len(graph))}
        for i in range(len(graph)):
            for j in range(len(graph[i])):
                adj[i].append(graph[i][j])
        color=[-1]*len(graph)
        for i in range(len(graph)):
            if color[i] == -1:
                if self.checkbipartite(adj,i,color,1)==False:
                    return False
        return True
a=isBipartite()
# print(a.isBipartite([[1,3],[0,2],[1,3],[0,2]]))

# import heapq
# class NetworkDelayTime:
#     # def networkDelayTime(self, times, n, k):
#     #     adj={i:[] for i in range(1,n+1)} 
#     #     for time in times:
#     #         u,v,w=time
#     #         adj[u].append((v,w))
#     #     distance=[float("inf")]*(n+1)
#     #     distance[k]=0
#     #     priority_queue = [(0, k)]
#     #     while priority_queue:
#     #         current_distance,curr_node=heapq.heappop(priority_queue)
#     #         if current_distance>distance[curr_node]:
#     #             continue
#     #         for neighbour,wieght in adj[curr_node]:
#     #             dist = distance[curr_node]+wieght
#     #             if dist < distance[neighbour]:
#     #                 distance[neighbour]=dist
#     #                 heapq.heappush(priority_queue, (dist, neighbour))
#     #     distance[0]=0
#     #     return -1 if max(distance)==float("inf") else max(distance)
#     def findCheapestPrice(self, n: int, flights, src, dst, k) -> int:
      
# a=NetworkDelayTime()
# print(a.networkDelayTime([[1,2,1]], n = 2, k = 2))

        

class MakeSolution:
    def dfs(self,adj,ans,product,visited,query1,query2):
        if query1 in visited:
            return
        visited.add(query1)
        if query1==query2:
            ans[0]=product
            return
        for v in adj[query1]:
            self.dfs(adj,ans,product*v[1],visited,v[0],query2)
    def calcEquation(self, equations, values, queries):
        adj={}
        for i in range(len(equations)):
            u=equations[i][0]
            v=equations[i][1]
            value=values[i]
            adj.setdefault(u, []).append((v, value))
            adj.setdefault(v, []).append((u, 1.0 / value))
        result=[]
        for querie in queries:
            query1,query2=querie
            ans=[-1.0]
            product=1
            visited=set()
            if query1 in adj:
                self.dfs(adj,ans,product,visited,query1,query2)
            else:
                ans[0]=-1.0
            result.append(ans[0])
        return result
a=MakeSolution()
# print(a.calcEquation(equations = [["a","b"],["b","c"]], values = [2.0,3.0], queries = [["a","c"],["b","a"],["a","e"],["a","a"],["x","x"]]
# ))

class Solution2:
    def findSmallestSetOfVertices(self, n, edges):
        indegree=[0]*n
        adj={i:[] for i in range(n)}
        for edge in edges:
            u,v=edge
            adj[u].append(v)
        for u in range(n):
            for v in adj[u]:
                indegree[v]+=1
        result=[]
        for i in range(len(indegree)):
            if indegree[i]==0:
                result.append(i)
        return result
    def maximalNetworkRank(self, n, roads):
        indegree=[0]*n
        adj={i:[] for i in range(n)}
        for edge in roads:
            u,v=edge
            indegree[u]+=1
            indegree[v]+=1
            adj[u].append(v)
            adj[v].append(u)
        maxS=0
        for i in range(n):
            for j in range(i+1,n):
                rank=indegree[i]+indegree[j]
                if j in adj[i]:
                    rank=-1
                maxS=max(maxS,rank)
        return maxS
        
a=Solution2()
# print(a.findSmallestSetOfVertices(n = 5, edges = [[0,1],[2,1],[3,1],[1,4],[2,4]]))
print(a.maximalNetworkRank(  8,[[4,6],[5,2],[3,5],[7,5],[7,6]]))
        
        
        
        





        

        