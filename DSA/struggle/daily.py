from collections import deque


def maxValue(events, k):
    events.sort(key=lambda x: x[0])
    dp = [[-1 for _ in range(k + 1)] for _ in range(len(events) + 1)]

    def linearSearch(events, index):
        start, end, weight = events[index]
        for i in range(index + 1, len(events)):
            if events[i][0] > end:
                return i
        return len(events)

    # def binarySearch(index):
    #     start = index
    #     end = len(events)
    #     while start < end:
    #         mid = start + (end - start) // 2

    def solve(events, index, k, dp):
        if index >= len(events) or k == 0:
            return 0
        if dp[index][k] != -1:
            return dp[index][k]
        aftertake = linearSearch(events, index) if linearSearch(events, index) else 0
        take = solve(events, aftertake, k - 1) + events[index][2]
        skip = solve(events, index + 1, k)
        dp[index][k] = max(take, skip)
        return dp[index][k]

    return solve(events, 0, k, dp)


def numBusesToDestination(routes, source, target):
    adj = {}
    if source == target:
        return 0
    for i in range(len(routes)):
        for j in range(len(routes[i])):
            if routes[i][j] in adj:
                adj[routes[i][j]].add(i)
            else:
                adj[routes[i][j]] = set()
    queue = deque()
    visited = set()
    for v in routes[source]:
        queue.append(v)
        visited.add(v)
    count = 1
    while queue:
        size = len(queue)
        while size:
            route = queue.popleft()
            for stop in route:
                if stop == target:
                    return count
                if stop in visited:
                    continue
                for nextroute in adj[stop]:
                    if nextroute in visited:
                        visited.add(nextroute)
                        queue.append(nextroute)
            size -= 1
        count += 1
    return -1


def slidingPuzzle(board):
    adj = {}
    start = ""
    for i in range(len(board)):
        for j in range(len(board[0])):
            start += str(board[i][j])
    adj[0] = {1, 3}
    adj[1] = {0, 2, 4}
    adj[2] = {1, 5}
    adj[3] = {0, 4}
    adj[4] = {1, 3, 5}
    adj[5] = {2, 4}
    visited = set()
    target = "123456"
    queue = deque()
    queue.append(start)
    steps = 0
    visited.add(start)

    def find(value):
        for i in range(len(value)):
            if value[i] == "0":
                return i

    while queue:
        size = len(queue)
        while size:
            value = queue.popleft()
            if value == target:
                return steps
            zero_index = find(value)
            for swapIdx in adj[zero_index]:
                state_list = list(value)
                state_list[zero_index], state_list[swapIdx] = (
                    state_list[swapIdx],
                    state_list[zero_index],
                )
                new_state = "".join(state_list)
                if new_state not in visited:
                    visited.add(new_state)
                    queue.append(new_state)
            size -= 1
        steps += 1
    return -1
