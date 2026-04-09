class GraphAdajencyMatrix:
    def __init__(self,vertices,):
        self.vertices=vertices
        self.graph=[[0]*vertices for _ in range(vertices)]
    
    def add(self,start,end):
        self.graph[start][end]=1
        self.graph[end][start]=1

    def print_graph(self):
        for row in self.graph:
            print(row)



graph=GraphAdajencyMatrix(5)
graph.add(0,1)
graph.add(1,1)
graph.add(0,2)
graph.add(1,2)
# graph.print_graph()



class GraphAdajencyList:
    def __init__(self,vertices):
        self.vertices=vertices
        self.graph={i:[] for i in range(vertices)}
    
    def add_edge(self,start,end):
        self.graph[start].append(end)
        self.graph[end].append(start)

    def print_graph(self):
        for vertex in self.graph:
            print(F"{vertex} : {self.graph}")


num_vertices = 5
graph = GraphAdajencyList(num_vertices)
graph.add_edge(0, 1)
graph.add_edge(0, 2)
graph.add_edge(1, 3)
graph.add_edge(3,4)
# graph.print_graph()


# def graph(arr):
#    a= {i:[] for i in range(len(arr))}
#    for item in arr:
#        v=item[1]
#        u=item[0]
#        a[u].append(v)
#     return a

# print(graph([[1,0],[2,0],[2,1],[3,1]]))
def graph(arr):
    a = {i: [] for i in range(len(arr))}
    for item in arr:
        v = item[1]
        u = item[0]
        a[u].append(v)
    return a

result = graph([[1, 0], [2, 0], [2, 1], [3, 1]])

def dfs(a,u,bool,result):
    if(bool[u]==True): return
    bool[u]=True
    result.append(u)
    for value in a[u]:
        if(bool[value]==False):
            dfs(a,value,bool,result)


def graph1(Vertex,arr):
    a={i:[] for i in range(Vertex)}
    for u,v in enumerate(arr):
            for n in v:
                a[u].append(n)
    my_array = [False for _ in range(Vertex)]
    result=[]
    dfs(a,0,my_array,result)
    return result
    

print(graph1(5,[[2,3,1],[0],[0,4],[0],[2]]))
from collections import deque

def bfs(a,u,my_array,result):
    queue=deque()
    queue.append(u)
    my_array[u]=True
    result.append(u)
    while queue:
        vertex=queue.popleft()
        for value in a[vertex]:
            if(my_array[value]==False):
                queue.append(value)
                my_array[value]=True
                result.append(value)

          
    # print(a,0,my_array,result)

def graph2(Vertex,arr):
    a={i:[] for i in range(Vertex)}
    for u,v in enumerate(arr):
            for n in v:
                a[u].append(n)
    my_array = [False for _ in range(Vertex)]
    result=[]
    bfs(a,0,my_array,result)
    return result


print(graph2(6,[[5,4],[0],[0,4],[0],[2]]))

def isCycleDfs(a,u,my_array,parent):
    my_array[u]=True
    for value in a[u]:
        if(value == parent): return True
        if(my_array[value]==True): return True
        if(isCycleDfs(a,value,my_array,u)):
            return True
    return False

def detectCycle(vertex,arr):
    a={i:[] for i in range(vertex)}
    for u,v in enumerate(arr):
            for n in v:
                a[u].append(n)
    my_array = [False for _ in range(vertex)]
    for i in range(vertex):
        if(my_array[i]==False and isCycleDfs(a,i,my_array,-1)):
            return True
    return False
                
    

print(detectCycle( 5,[[1] ,[ 0, 2,4], [1 ,3],[ 2, 4],[1,3]] ))
print(detectCycle(4,  [[1], [2], [3], []]))
    

from collections import defaultdict
from collections import deque
class DetechGraph:
    def __init__(self,vertex):
        self.vertices=vertex
        self.graph=defaultdict(list)

    def addEdge(self,v,w):
        self.graph[v].append(w)
        self.graph[w].append(v)

    def isCycleDfs(self,v,visited,parent):
        visited[v]=True
        for value in self.graph[v]:
            if(value == parent): return True
            if(visited[value]==True): return True
            if(isCycleDfs(self.graph,value,visited,v)):
                return True
        return False
    
def isCycle(self):
        visisted=[False]*(self.vertices)
        for i in range(self.vertices):
            if(visisted[i]==False and isCycleDfs(self,i,visisted,-1)):
                return True
            
        return False

def isCycleBfs(a,u,visited):
    queue=deque()
    queue.append({u,-1})
    visited[u]=True
    while(len(queue)!=0):
        value=queue.popleft()
        value_list=list(value)
        first_Value=value_list[0]
        second_Value=value_list[1]
        for value in a[first_Value]:
            if(visited[value]==False):
                visited[value]=True
                queue.append({value,first_Value})
            elif(value !=second_Value):
                return True
    return False

def cycleBfs(vertex,arr):
    visited=[False]*(vertex)
    a={i:[] for i in range(vertex)}
    for u,v in enumerate(arr):
            for n in v:
                a[u].append(n)
    for i in range(vertex):
        if(visited[i]==False and isCycleBfs(a,i , visited)):
            return True
    return False
print(cycleBfs( 5,[[1] ,[ 0, 2,4], [1 ,3],[ 2, 4],[1,3]] ))
print(cycleBfs(4,  [[1], [2], [3], []]))

def isCycleDirectDfs(a,u,visited,inrecursion):
    visited[u]=True
    inrecursion[u]=True
    for value in a[u]:
        if(visited[u]==False):
            if(isCycleDirectDfs(a,value,visited,inrecursion)==True):
                return True
            elif(inrecursion[value]==True):
                return True
    inrecursion[u]=False
    return False

def isCycleDirectedDfs(vertex,arr):
    visited=[False]*(vertex)
    inrecursion=[False]*(vertex)
    a={i:[] for i in range(vertex)}
    for u,v in enumerate(arr):
            for n in v:
                a[u].append(n)
    for i in range(vertex):
        if(visited[i]==False and isCycleDirectDfs(a,i , visited,inrecursion)):
            return True
    return False

def detectCycleDfsDirect(a, u, my_array, inrecursion):
    my_array[u] = True
    inrecursion[u] = True
    for value in a[u]:
        if my_array[value] == False:
            if detectCycleDfsDirect(a, value, my_array, inrecursion):
                return True
        elif inrecursion[value] == True:
            return True
    inrecursion[u] = False
    return False

def detectCycleDirectedDfs(vertex, adj):
    a = {i: [] for i in range(vertex)}
    for u, v in enumerate(adj):
        for n in v:
            a[u].append(n)
    my_array = [False for _ in range(vertex)]
    inrecursion = [False for _ in range(vertex)]
    for i in range(vertex):
        if my_array[i] == False and detectCycleDfsDirect(a, i, my_array, inrecursion):
            return True

    return False

print(detectCycleDirectedDfs(6, [
    [1],
    [2, 3],
    [4],
    [5],
    [],
    []
]))
print(detectCycleDirectedDfs(6,[ [1],[2],[0],[4], [3]]
))
print(detectCycleDirectedDfs(2,[[1,0]]),"joojoo")
print(detectCycleDirectedDfs(2,[[0,1],[1,0]]),"joo")
