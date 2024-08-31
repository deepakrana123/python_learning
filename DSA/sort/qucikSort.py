def qucikSort(arr,low,high):
    if(low>=high): return
    p=partition(arr,low,high)
    qucikSort(arr,low,p-1)
    qucikSort(arr,p+1,high)
    
    
def partition(arr,low,high):
    pivot=arr[high]
    i=0
    pivot_index=0
    
    for i in range(len(arr)):
        if arr[i]<pivot:
            temp=arr[i]
            arr[i]=arr[pivot_index]
            arr[pivot_index]=temp
            pivot_index+=1
    temp=arr[high]
    arr[high]=arr[pivot_index]
    arr[pivot_index]=temp
    return pivot_index
        
    