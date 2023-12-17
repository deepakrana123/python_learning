import heapq

class Graph:
    def __init__(self, vertices):
        self.V = vertices
        self.graph = {i: [] for i in range(self.V)}

    def add_edge(self, src, dest, weight):
        self.graph[src].append((dest, weight))
        self.graph[dest].append((src, weight))  # For undirected graph

    def prim_mst(self):
        visited = [False] * self.V
        min_heap = []
        mst_cost = 0
        mst = []

        heapq.heappush(min_heap, (0, 0))  # Start with vertex 0 and weight 0

        while min_heap:
            weight, vertex = heapq.heappop(min_heap)

            if not visited[vertex]:
                visited[vertex] = True
                mst_cost += weight

                for neighbor, edge_weight in self.graph[vertex]:
                    if not visited[neighbor]:
                        heapq.heappush(min_heap, (edge_weight, neighbor))
                        mst.append((vertex, neighbor, edge_weight))

        return mst, mst_cost

# Example Usage:
g = Graph(5)
g.add_edge(0, 1, 2)
g.add_edge(0, 3, 6)
g.add_edge(1, 2, 3)
g.add_edge(1, 3, 8)
g.add_edge(1, 4, 5)
g.add_edge(2, 4, 7)
g.add_edge(3, 4, 9)

mst_edges, mst_cost = g.prim_mst()
print("Edges in MST:")
for edge in mst_edges:
    print(edge)
print("Total cost of MST:", mst_cost)
