print("hiii")
# import queue

# def diji(source,adj):
#     piortiy=queue.PriorityQueue()
#     result={node: float('inf') for node in adj}
#     result[source]=0
#     piortiy.put((0,source))
#     while not piortiy.empty:
#         d,node=piortiy.get()

#         for distance , adjNode in enumerate(adj[node]):
#             if(d+distance<result[adjNode]):
#                 result[adjNode]=d+distance
#                 piortiy.put((d+distance , adjNode))
#     return result


# c=diji('A',{
#     'A': {'B': 2, 'C': 4},
#     'B': {'C': 1, 'D': 7},
#     'C': {'D': 3},
#     'D': {'E': 2},
#     'E': {}
# }
# )

# print(c)


import heapq

def dijkstra(graph, start):
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    priority_queue = [(0, start)]
    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)
        if current_distance > distances[current_node]:
            continue
        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(priority_queue, (distance, neighbor))
    return distances

# Example graph representation (dictionary of dictionaries)
# Format: {node: {neighbor: weight, ...}, ...}
graph = {
    'A': {'B': 2, 'C': 4},
    'B': {'C': 1, 'D': 7},
    'C': {'D': 3},
    'D': {'E': 2},
    'E': {}
}

start_node = 'A'
shortest_distances = dijkstra(graph, start_node)
print(f"Shortest distances from node {start_node}: {shortest_distances}")


def dijkstra(graph, start):
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    unvisited = set(graph.keys())
    while unvisited:
        current_node = min(unvisited, key=lambda node: distances[node])
        unvisited.remove(current_node)

        for neighbor, weight in graph[current_node].items():
            distance = distances[current_node] + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance

    return distances

# Example graph representation (dictionary of dictionaries)
# Format: {node: {neighbor: weight, ...}, ...}
graph = {
    'A': {'B': 2, 'C': 4},
    'B': {'C': 1, 'D': 7},
    'C': {'D': 3},
    'D': {'E': 2},
    'E': {}
}

start_node = 'A'
shortest_distances = dijkstra(graph, start_node)
print(f"Shortest distances from node {start_node}: {shortest_distances}")
