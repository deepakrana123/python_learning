# # class GraphAdjancyMatrix:
# #     def __init__(self, vertex):
# #         self.vertex = vertex
# #         self.graph = [[0]*vertex for _ in range(vertex)]

# #     def add(self, start, end):
# #         self.graph[start][end] = 1
# #         self.graph[end][start] = 1

# #     def print(self):
# #         for i in self.graph:
# #             print(i)


# # graph = GraphAdjancyMatrix(5)
# # graph.add(0, 1)
# # graph.add(1, 1)
# # graph.add(0, 2)
# # graph.add(1, 2)
# # # graph.print()

# # adj = [[0, 1], [1, 1], [0, 2], [1, 2]]


# # def adjanceyMatrix(vertex, adj):
# #     graph = [[0]*vertex for _ in range(vertex)]
# #     for u, v in enumerate(adj):
# #         graph[v[0]][v[1]] = 1
# #         graph[v[1]][v[0]] = 1
# #     return graph


# # # print(adjanceyMatrix(5, adj))


# # def adjanceyList(adj):
# #     graph = {i: [] for i in range(len(adj))}
# #     for item in adj:
# #         v = item[1]
# #         u = item[0]
# #         graph[u].append(v)
# #     return graph


# # print(adjanceyList(adj))


# # class adjanceyLists:
# #     def __init__(self, vertex):
# #         self.vertex = vertex
# #         self.graph = {i: [] for i in range(vertex)}

# #     def add(self, start, end):
# #         self.graph[start].append(end)
# #         self.graph[end].append(start)

# #     def print(self):
# #         for item in self.graph:
# #             print(item, self.graph)


# # graph1 = adjanceyLists(5)
# # graph1.add(0, 1)
# # graph1.add(1, 1)
# # graph1.add(0, 2)
# # graph1.add(1, 2)
# # # graph1.print()


# # # lets do depth first search

# # def dfs(adj, u, vis, result):
# #     vis[u] = True
# #     result.append(u)
# #     for u, v in enumerate(adj):
# #         for value in v:
# #             if (vis[value] == False):
# #                 dfs(adj, value, vis, result)


# # def depthfirstSearch(vertex, adj):
# #     graph = {i: [] for i in range(len(adj))}
# #     vis = [False for _ in range(vertex)]
# #     for item in adj:
# #         v = item[1]
# #         u = item[0]
# #         graph[u].append(v)
# #     result = []
# #     dfs(adj, 0, vis, result)
# #     return result
# # from collections import deque
# # def bfs(a,u,vis,result):
# #     quque=deque()
# #     quque.append(u)
# #     vis[u]=True
# #     result.append(u)
# #     while(len(quque)!=0):
# #         f=quque.popleft()
# #         for value in a[f]:
# #             if(vis[value]==False):
# #                 quque.append(value)
# #                 vis[value]=True
# #                 result.append(value)



# # def breathfirstSearch(vertex,adj):
# #     a={i:[] for i in range(vertex)}
# #     for u,v in enumerate(adj):
# #             for n in v:
# #                 a[u].append(n)
# #     my_array = [False for _ in range(vertex)]
# #     result=[]
# #     bfs(a,0,my_array,result)
# #     return result

# # def dfsUnDirectCycle(adj,u,vis,parent):
# #     vis[u]=True
# #     for value in adj[u]:
# #         if(value==parent):continue
# #         if(vis[u]==True):return True
# #         if(dfsUnDirectCycle(adj,value,vis,u)):return True
# #     return False
# # def detectCycleUndirectedDfs(vertex,adj):
# #     a={i:[] for i in range(vertex)}
# #     for u,v in enumerate(adj):
# #             for n in v:
# #                 a[u].append(n)
# #     my_array = [False for _ in range(vertex)]
# #     for i in range(vertex):
# #         if(my_array[i]==False and dfsUnDirectCycle(a,0,my_array,-1)):
# #             return True
    
# #     return False

# # def bfsUnDirectCycle(adj,u,vis):
# #     queue=deque()
# #     queue({u,-1})
# #     vis[u]=True
# #     while(len(queue)!=0):
# #         value=queue.popleft()
# #         value_list=list(value)
# #         soucre=value_list[0]
# #         parent=value_list[1]
# #         for v in adj[soucre]:
# #             if(vis[v]==False):
# #                 vis[v]=True
# #                 queue.append({v,soucre})
# #             elif(v!=parent):
# #                 return True
# #     return False


# # def detectCycleUndirectedBfs(vertex,adj):
# #     a={i:[] for i in range(vertex)}
# #     for u,v in enumerate(adj):
# #             for n in v:
# #                 a[u].append(n)
# #     my_array = [False for _ in range(vertex)]
# #     for i in range(vertex):
# #         if(my_array[i]==False and bfsUnDirectCycle(a,0,my_array)):
# #             return True
    
# #     return False
# # def detectCycleDfsDirect(a,u,my_array,inrecusrion):
# #     my_array[u]=True
# #     inrecusrion[u]=True
# #     for value in a[u]:
# #         if(my_array[value]==False and detectCycleDfsDirect(a,value,my_array,inrecusrion)):
# #             return True
# #         elif(inrecusrion[value]==True):
# #             return True
# #     inrecusrion[u]=False
# #     return False



# # def detectCycleDirectedDfs(vertex,adj):
# #     a={i:[] for i in range(vertex)}
# #     for u,v in enumerate(adj):
# #             for n in v:
# #                 a[u].append(n)
# #     my_array = [False for _ in range(vertex)]
# #     inrecusrion=[False for _ in range(vertex)]
# #     for i in range(vertex):
# #         if(my_array[i]==False and dfsUnDirectCycle(a,0,my_array,inrecusrion)):
# #             return True
    
# #     return False


# # # print(detectCycleDirectedDfs(2,[[1,0]]))

# # def toposortDfsCycle (a,u,my_array,stack):
# #     my_array[u]=True
# #     for value in a[u]:
# #         if(my_array[value]==False):
# #             toposortDfs(a,value,my_array,stack)
# #     stack.append(u)



# # def toposortDfs(vertex,adj):
# #     a={i:[] for i in range(vertex)}
# #     stack=[]
# #     for u,v in enumerate(adj):
# #         for n in v:
# #             a[u].append(n)
# #     my_array = [False for _ in range(vertex)]
# #     for i in range(vertex):
# #         if(my_array[i]==False):
# #             toposortDfsCycle(a,0,my_array,stack)
# #     result=[]
# #     while(len(stack)!=0):
# #         result.append(stack[len(stack)-1])
# #         stack.pop()
# #     return result  

# # from collections import deque

# # def topoSort(vertex, adj):
# #     a = {i: [] for i in range(vertex)}
# #     queue = deque()
# #     indegree = [0 for _ in range(vertex)]
# #     for u, v in enumerate(adj):
# #         for n in v:
# #             a[u].append(n)
# #     for u in range(vertex):
# #         for n in adj[u]:
# #             indegree[n] = indegree[n] + 1
# #     for u in range(vertex):
# #         if indegree[u] == 0:
# #             queue.append(u)

# #     result = []
# #     count=0
# #     while len(queue) != 0:
# #         v = queue.popleft()
# #         result.append(v)
# #         for u in a[v]:
# #             indegree[u] = indegree[u] - 1
# #             if indegree[u] == 0:
# #                 count=count+1
# #                 queue.append(u)
# #     return result

# from collections import deque
# # from collections import deque
# from typing import List

# class Solution:
#     def toposort(self,adj,numCourses,indegree):
#         print(adj,numCourses,indegree)
#         queue=deque()
#         count=0
#         for u in range(numCourses):
#             if(indegree[u]==0):
#                 count=count+1
#                 queue.append(u)
#         while(len(queue) !=0):
#             v=queue.popleft()
#             for u in adj[v]:
#                 indegree[u]-=1
#                 if(indegree[u]==0):
#                     count+=1
#                     queue.append(u)
#         print(count)
#         return count == numCourses:
#             
#     def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
#         a={i:[] for i in range(numCourses)}
#         indegree=[0]*numCourses
#         for v ,u in prerequisites:
#             a[u].append(v)
#             indegree[b]+=1
#         return self.toposort(a,numCourses,indegree)
            

# p=Solution()
# print(p.canFinish(2,[[1,0]]))        
        

prerequisites=[[1,0],[0,1]]
for course, prereq in prerequisites:
    print(course , prereq)

            # adj[prereq].append(course)
    