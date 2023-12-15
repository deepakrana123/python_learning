class AdjanceyMatrix:
    def __init__(self,vertex):
        self.vertex=vertex
        self.adj=[[0]*vertex for i in range(vertex)]
    
    def add(self,start,end):
        self.adj[start][end]=1
        self.adj[end][start]=1
    
    def print(self):
        for u in range(self.adj):
            print(u)

class AdjanceList:
    def __init__(self,vertex):
        self.vertex=vertex
        self.adj={i:[] for i in range(vertex)}

    def add(self,start,end):
        self.adj[start].append(end)
        self.adj[end].append(start)
    
    def print(self):
        for vertex in self.adj:
            print(vertex,"vertex")
        

def graphList(arr):
    adj={i:[] for i in range(len(arr))}
    for u,v in enumerate(arr):
        adj[u].append(v)
    return adj

def graphMatrix(arr):
    adj=[[0]*len(arr) for i in range(len(arr))]
    for u in range(len(arr)):
        x=arr[u][0]
        y=arr[u][1]
        adj[x][y]=1
        adj[y][x]=1
    return adj

print(graphList([[1,0],[2,0],[2,1],[3,1]]))
print(graphMatrix([[1,0],[2,0],[2,1],[3,1]]))

def dfs(adj,u,result,arr):
    if(result[u]==True): return
    result[u]=True
    arr.append(u)
    for v in adj[u]:
        dfs(adj,v,result,arr)

def dfsSearch(vertex,arr):
    adj={i:[] for i in range(vertex)}
    for u,v in enumerate(arr):
        for n in v:
            adj[u].append(n)
    result=[False]*(vertex)
    arr=[]
    dfs(adj,0,result,arr)
    return arr

print(dfsSearch(4,[[1,0],[2,0],[2,1],[3,1]]))

from collections import deque
def bfsSearch(adj,u,result,bool):
    queue=deque()
    queue.append(u)
    bool[u]=True
    result.append(u)
    for value in adj[u]:
        if(bool[value]==True): return
        elif(bool[value]==False):
            queue.append(value)
            bool[value]=True
            result.append(value)
    return result



def graph2(vertex,arr):
    adj={i:[] for i in range(vertex)}
    for u,v in enumerate(arr):
        for n in v:
            adj[u].append(n)
    bool=[False]*vertex
    result=[]
    bfsSearch(adj,0,result,bool)
    return result


