def binarySearch(arr,k):
    left=0
    right=len(arr)-1
    while(left<right):
        mid = (right + left) // 2
        if arr[mid]==k:
            return mid
        elif arr[mid]<k:
            left=mid+1
        else:
            right=mid-1
    return -1
def lowerbound(arr,k):
    left=0
    right=len(arr)-1
    ans=-1
    while(left<=right):
        mid = (right + left) // 2
        if arr[mid]>=k:
            ans=mid
            right=mid-1
        else:
            left=mid+1
    return arr[ans]
print(lowerbound([3, 4, 4, 7, 8, 10],8))
def upperBound(arr,k):
    left=0
    right=len(arr)-1
    ans=-1
    while(left<right):
        mid = (right + left) // 2
        if arr[mid]<=k:
            ans=-1
            left=mid+1
        else:
            right=mid-1
    return ans
            
def floow(arr,k):  
    left=0
    right=len(arr)-1
    ans=-1
    while(left<=right):
        mid = (right + left) // 2
        if arr[mid]<=k:
            ans=mid
            left=mid+1
        else:
            right=mid+1
    return arr[ans]
    