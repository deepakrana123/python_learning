a=[2,-1,3,-2,4,6,7]


def cyclicrotation(arr):
    temp=arr[len(arr)-1]
    for i in range(len(arr)-1,0,-1):
        arr[i]=arr[i-1]
    arr[0]=temp
    return arr


print(cyclicrotation([2,-1,3,-2,4,6,7]))

def kadaneAlgorithim(arr):
 max=0
 for i  in range(0,len(arr)):
    sum=0
    for j in range(i,len(arr)):
       sum=sum+arr[j]

       if(sum>max):
          max=sum
       
 return max

print(kadaneAlgorithim([1,2,3,-6,-2,5,1]))
    