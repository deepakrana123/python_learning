def sort(arr):
    for i in range(0,len(arr)-1):
         for j in range(i+1,len(arr)):
            if(arr[i]>arr[j]):
                temp=arr[i]
                arr[i]=arr[j]
                arr[j]=temp
            
    return arr

print(sort([0,1,0,2,1,2,3,0]))


def sort1(arr):
    n=len(arr)
    count0=0
    count1=0
    count2=0
    for i in range(0,len(arr)):
        if(arr[i]==0):
            count0=count0+1
        if(arr[i]==1):
            count1=count1+1
        if(arr[i]==2):
            count2=count2+1
        print(count1,count2,count0)
    for i in range(0,count0):
        arr[i]=0
    for i in range(count0,(count0+count1)):
        arr[i]=1
    for i in range((count1+count0),n):
        arr[i]=2


    return arr   


print(sort1([0, 2, 1, 1, 0, 2]))