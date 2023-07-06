a=[2,-1,3,-2,4,6,7]


def cyclicrotation(arr):
    temp=arr[len(arr)-1]
    for i in range(len(arr)-1,0,-1):
        arr[i]=arr[i-1]
    arr[0]=temp
    return arr


print(cyclicrotation([2,-1,3,-2,4,6,7]))

def kadaneAlgorithim(arr):
    