def numSubmatrixSumTarget(matrix, target=0):
    for i in range(len(matrix)):
        for j in range(1, len(matrix[0])):
            matrix[i][j] = matrix[i][j] + matrix[i][j - 1]
    for j in range(len(matrix[0])):
        hasmap = {0: 1}
        for i in range(len(matrix)):
            continue


print(numSubmatrixSumTarget([[0, 1, 0], [1, 1, 1], [0, 1, 0]]))
