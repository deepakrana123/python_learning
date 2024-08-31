def kthSmallestPrimeFraction(arr, k):
    a=[]
    for i in range(len(arr)):
        for j in range(i+1,len(arr)):
            a.append({arr[i],arr[j]})
    print(a)
print(kthSmallestPrimeFraction([1,2,3,5],3))