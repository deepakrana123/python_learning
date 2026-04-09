from collections import deque


def timeRequiredToBuy(tickets, k):
    count = 0
    for i in range(len(tickets)):
        if i <= k and tickets[i] <= tickets[k]:
            count += min(tickets[i], tickets[k])
        elif i <= k and tickets[i] > tickets[k]:
            count += min(tickets[i], tickets[k])
    return count


def deckRevealedIncreasing(deck):
    deck.sort()
    a = [0]*len(deck)
    # j=0
    # i=0
    # skip=False
    # while(i<len(deck)):
    #     if a[j]==0:
    #         if skip==False:
    #             a[j]=deck[i]
    #             i+=1
    #         skip=not skip
    #     j=(j+1)%len(deck)
    # return a
    queue = deque([])
    for i in range(len(deck)):
        queue.append(i)
    for i in range(len(deck)):
        d = queue.popleft()
        a[d] = deck[i]
        if (queue):
            e = queue.popleft()
            queue.append(e)

    return a


def removeKdigits(num, k):
    a = []
    for i in range(len(num)):
        if len(a) > 0 and a[len(a)-1] > num[i] and k > 0:
            print(num[i], "a")
            a.pop()
            k = k-1
        elif a or num[i] != 0:
            a.append(num[i])
    print(a, k)
    while k > 0 and a:
        a.pop()
        k -= 1
    if len(a) == 0:
        return 0
    return "".join(a)


def solve(n, count, arr1, arr2, index):
    if index > n or n == 0:
        return count
    while (index <= n):
        if (index-1) % 2 == 0:
            count = 1+solve(n-1, count, arr1, arr2, index+1)


def solve(x, y):
    mod = pow(10, 9)+7
    if y == 0:
        return 1
    ans = solve(x, y//2)
    ans *= ans
    ans %= mod
    if y % 2 != 0:
        ans *= x
        ans %= mod
    return ans


def countGoodNumbers(n):
    count = 0
    arr1 = [0, 2, 4, 6, 8]
    arr2 = [2, 3, 5, 7]
    # return solve(n,count,arr1,arr2,0)
    even = n//2 + n % 2
    odd = n//2
    mod = pow(10, 9)+7
    return (pow(5, even)*pow(4, odd)) % mod


print(countGoodNumbers(50))


def bfs(a, index, visited):
    queue = deque()
    queue.append(index)
    visited[index] = True
    while queue:
        d = queue.popleft()
        for v in a[d]:
            if visited[v] == False:
                bfs(a, v, visited)


def findCircleNum(isConnected):
    a = {i: [] for i in range(len(isConnected))}
    for i in range(len(isConnected)):
        for j in range(len(isConnected[0])):
            if isConnected[i][j] == 1:
                a[i].append(j)
                a[j].append(i)

    visited = [False]*len(isConnected)
    count = 0
    for i in range(len(isConnected)):
        if visited[i] == False:
            bfs(a, i, visited)
            count += 1
    return count


def dfs(matrix, i, j, perimeter, m, n):
    if i < 0 or i >= m or j < 0 or j <= n or matrix[i][j] == 0:
        perimeter += 1
        return
    if matrix[i][j] == -1:
        return
    matrix[i][j] = -1
    dfs(matrix, i-1, j, perimeter, m, n)
    dfs(matrix, i, j-1, perimeter, m, n)
    dfs(matrix, i, j+1, perimeter, m, n)
    dfs(matrix, i+1, j, perimeter, m, n)


def isLandPerimeter(matrix):
    m = len(matrix)
    n = len(matrix[0])
    perimeter = 0
    for i in range(len(m)):
        for j in range(len(n)):
            if matrix[i][j] == 1:
                dfs(matrix, i, j, perimeter, m, n)
                return perimeter
    return -1


def dfsNumberOfIsLand(matrix, i, j, m, n):
    if i < 0 or i >= m or j < 0 or j <= n or matrix[i][j] == 0:
        return
    if matrix[i][j] == -1:
        return
    matrix[i][j] = -1
    dfsNumberOfIsLand(matrix, i-1, j, m, n)
    dfsNumberOfIsLand(matrix, i, j-1, m, n)
    dfsNumberOfIsLand(matrix, i, j+1, m, n)
    dfsNumberOfIsLand(matrix, i+1, j, m, n)


def numberOfIsland(matrix):
    m = len(matrix)
    n = len(matrix[0])
    count = 0
    for i in range(len(m)):
        for j in range(len(n)):
            if matrix[i][j] == 1:
                dfs(matrix, i, j, m, n)
                count += 1
    return count
