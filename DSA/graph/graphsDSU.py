# operation to find two set
# two members are disjoint or being to same set or not


class DisjointSetUnion:
    def __init__(self, n):
        self.parent = [i for i in range(n)]
        self.rank = [0] * n  # To optimize union by rank

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # Path compression
        return self.parent[x]

    def union(self, x, y):
        root_x = self.find(x)
        root_y = self.find(y)

        if root_x != root_y:
            # Union by rank
            if self.rank[root_x] < self.rank[root_y]:
                self.parent[root_x] = root_y
            elif self.rank[root_x] > self.rank[root_y]:
                self.parent[root_y] = root_x
            else:
                self.parent[root_y] = root_x
                self.rank[root_x] += 1


# Creating a Disjoint Set Union instance with 5 elements
dsu = DisjointSetUnion(5)

# Performing unions
dsu.union(0, 2)
dsu.union(1, 4)
dsu.union(3, 2)

# Finding roots
print(dsu.find(0))  # Output: 2 (representative/root of set containing element 0)
print(dsu.find(1))  # Output: 4 (representative/root of set containing element 1)
print(dsu.find(3))  # Output: 2 (representative/root of set containing element 3)


class DisjointSetUnion:
    def __init__(self, n):
        self.parent = [i for i in range(n)]
        self.rank = [0] * n  # To optimize union by rank

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # Path compression
        return self.parent[x]

    def union(self, x, y):
        root_x = self.find(x)
        root_y = self.find(y)
        if root_x != root_y:
            # Union by rank
            if self.rank[root_x] < self.rank[root_y]:
                self.parent[root_x] = root_y
            elif self.rank[root_x] > self.rank[root_y]:
                self.parent[root_y] = root_x
            else:
                self.parent[root_y] = root_x
                self.rank[root_x] += 1
        else:
            return True  # Cycle detected when both vertices have the same root
        return False


def has_cycle(graph_edges, num_vertices):
    dsu = DisjointSetUnion(num_vertices)
    for edge in graph_edges:
        if dsu.union(edge[0], edge[1]):
            return True  # Cycle detected
    return False  # No cycle detected


# Example usage
edges = [(0, 1), (1, 2), (2, 3), (3, 0)]  # Define the edges of the graph
num_vertices = 4  # Number of vertices in the graph

if has_cycle(edges, num_vertices):
    print("The graph contains a cycle.")
else:
    print("The graph does not contain a cycle.")
