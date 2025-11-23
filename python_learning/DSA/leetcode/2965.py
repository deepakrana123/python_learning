def findMissingAndRepeatedValues(grid):
    dicts = {}
    n = len(grid)
    sums = sum([i for i in range(1, n * n + 1)])
    sqSums = sum([i * i for i in range(1, n * n + 1)])
    gridSum = 0
    gridSq = 0
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            gridSum += grid[i][j]
            gridSq += grid[i][j] * grid[i][j]

    t = gridSum - sums
    s = gridSq - sqSums
    c = s // t
    return [(t + c) // 2, (c - t) // 2]


print(findMissingAndRepeatedValues([[9, 1, 7], [8, 9, 2], [3, 4, 6]]))
