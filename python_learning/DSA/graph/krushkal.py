class Kruskal:
    def __init__(self, vertices):
        self.V = vertices
        self.graph = []

    def add_edge(self, u, v, w):
        self.graph.append([u, v, w])

    def find_parent(self, parent, i):
        if parent[i] == i:
            return i
        return self.find_parent(parent, parent[i])

    def union(self, parent, rank, x, y):
        xroot = self.find_parent(parent, x)
        yroot = self.find_parent(parent, y)

        if rank[xroot] < rank[yroot]:
            parent[xroot] = yroot
        elif rank[xroot] > rank[yroot]:
            parent[yroot] = xroot
        else:
            parent[yroot] = xroot
            rank[xroot] += 1

    def kruskal_algorithm(self):
        result = []
        i, e = 0, 0
        self.graph = sorted(self.graph, key=lambda item: item[2])
        parent = []
        rank = []
        for node in range(self.V):
            parent.append(node)
            rank.append(0)

        while e < self.V - 1:
            u, v, w = self.graph[i]
            i += 1
            x = self.find_parent(parent, u)
            y = self.find_parent(parent, v)
            if x != y:
                e += 1
                result.append([u, v, w])
                self.union(parent, rank, x, y)

        return result


# Example usage:
g = Kruskal(4)
g.add_edge(0, 1, 10)
g.add_edge(0, 2, 6)
g.add_edge(0, 3, 5)
g.add_edge(1, 3, 15)
g.add_edge(2, 3, 4)

# print("Edges of the minimum spanning tree:")
# print(g.kruskal_algorithm())

def find_parent(parent, i):
        if parent[i] == i:
            return i
        return find_parent(parent, parent[i])

def union(parent, rank, x, y):
        xroot = find_parent(parent, x)
        yroot = find_parent(parent, y)

        if rank[xroot] < rank[yroot]:
            parent[xroot] = yroot
        elif rank[xroot] > rank[yroot]:
            parent[yroot] = xroot
        else:
            parent[yroot] = xroot
            rank[xroot] += 1

def krushkalWeight(V,arr):
    adj=[]
    for value in arr:
        u=value[0]
        v=value[1]
        weight=value[2]
        adj.append([u,v,weight])
    adj=sorted(adj,key=lambda item:item[2])
    parent = []
    rank = []
    for node in range(V+1):
        parent.append(node)
        rank.append(0)
    sum=0
    i, e = 0, 0
    result=[]
    while e < V-1:
        u,v,w=adj[i]
        i=i+1
        parent_x=find_parent(parent,u)
        parent_y=find_parent(parent,v)
        if parent_x !=parent_y:
            sum+=w
            e+=1
            result.append([u,v,w])
            union(parent,rank,u,v)
    return sum
        
    
print(krushkalWeight(5, [[0,1,1],[1,2,1],[2,3,2],[0,3,2],[0,4,3],[3,4,3],[1,4,6]]))

    
        
   
    