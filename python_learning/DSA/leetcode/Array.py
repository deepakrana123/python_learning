def reverseanArray():
    arr=[1,2,3,4,5,6,7]
    ar=[]
    for i in range(len(arr)-1,-1,-1):
        ar.append(arr[i])
    return ar

# print(reverseanArray())

arr=[1,2,3,4,5,6,7]
# print(arr[::-1])
# print(arr.reverse())

def maxandmin():
    arrs=[5,1,2,0,4,8,7]
    max=-10000
    min=10000
    for i in range(0,len(arrs),1):
        if(arrs[i]>max):
            max=arrs[i]
        if(arrs[i]<min):
            min=arrs[i]

    return (max,min)


def findthekth(k):
    arr=[2,4,5,8,7,1,3]
    arr.sort()
    s=set(arr)
    print(arr,s)
    return arr[k-1]

print(findthekth(4))

