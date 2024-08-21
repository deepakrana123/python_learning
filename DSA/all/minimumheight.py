def minimum(arr,k):
    arr.sort()
    start=0
    end=len(arr)
    ar=[]
    mid=int(start +(end-start)/2)
    print(mid)
    for i in range(0,len(arr)):
       if(i<mid):
           ar.append(arr[i]+k)
       else:
           ar.append(arr[i]-k)
    return ar[len(ar)-1]-ar[0]
    print(ar)
   
print(minimum([1 ,5, 8, 10],2))
