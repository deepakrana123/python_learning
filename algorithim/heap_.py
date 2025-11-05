import heapq


def mincostToHireWorkers(quality, wage, k: int) -> float:
    heap = []
    for i in range(len(quality)):
        heapq.heappush(heap, (quality[i], quality[i], wage[i]))
    while heap:
        
    print(heap)


print(mincostToHireWorkers([10, 20, 5], [70, 50, 30], 2))
