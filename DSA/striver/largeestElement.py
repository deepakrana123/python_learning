def largeElement(arr):
    return max(arr)
def largeElement1(arr):
    a=float("-inf")
    for num in arr:
        if num>a:
            a=num
    return a
def largeElement2(arr):
    a=sorted(arr)
    return a[-1]
def secondLarestElement(arr):
    a=sorted(arr)
    return a[-2]
def secondLargestElement1(arr):
    a=float("-inf")
    b=float("-inf")
    if len(arr)<2:
        return -1
    for num in arr:
        if num>a:
            b=a
            a=num
        elif num>b and num!=a:
            b=num
    return {a,b}
def bySorted(arr):
    for i in range(1,len(arr)):
        if arr[i-1]>arr[i]:
            return False
    return True
def bySorted1(arr):
    for i in range(len(arr)):
        for j in range(i+1,len(arr)):
            if arr[j]<arr[i]:
                return False
    return True
a1=largeElement1({2,5,1,3,0})
a=largeElement({2,5,1,3,0})
b=secondLarestElement([2,5,1,3,0])
a2=largeElement2([2,5,1,3,0])
b1=secondLargestElement1([2,5,1,3,0])
b3=bySorted( [1, 2, 3, 4, 5])
b4=bySorted1( [1, 2, 3, 4, 5])


print(b3,b4)
    
            
   
