
def construct2DArray(original, m, n):
    if len(original) != n*m:
        return []
    a = [0]*(m)
    k = 0
    j = n
    for i in range(m):
        print(k,j,m)
        a[i] = original[k:j]
        k = j
        j = n+k
    return a

print(construct2DArray([4,5,1],3,1))
