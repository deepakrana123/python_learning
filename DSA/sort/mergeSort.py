def mergeSort(arr,l,r):
    if l==r:return 
    mid=int(l+(r-l)/2)
    mergeSort(arr,l,mid)
    mergeSort(arr,mid+1,r)
    merge(arr,l,mid,r)
    
def merge(arr,l,m,r):
    l1=m-l+1
    r1=r-m
    L=[]*(m-l+1)
    R=[]*(r-m)
    k=l
    for i in range(l1):
        L[i]=arr[k]
        k+=1
    for j in range(r1):
        R[i]=arr[k]
        k+=1
    i=l
    j=r
    y=0
    while(i<l1 and j<r1):
        if(L[i]<=R[j]):
            arr[k]=arr[i]
            k+=1
            j+=1
        elif L[i]>R[j]:
            L[i]=R[j]
            j+=1
            k+=1
    while i<l1:
        arr[k]=arr[i]
        k+=1
        i+=1
    while j<r1:
        arr[k]=arr[j]
        j+=1
        k+=1
    
        
            
        