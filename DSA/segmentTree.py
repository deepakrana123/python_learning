def updateLazyPropagtion(start,end,val,nums):
    n=len(nums)
    segmentTree=[0]*4*n
    lazyTree=[0]*4*n
    def updateSegmentTree(start,end,i,l,r,val,segmentTree,lazyTree):
        if lazyTree[i]!=0:
            segmentTree[i]+=(r-l+1)*lazyTree[i]
            if l!=r:
                lazyTree[2*i+1]=(r-l+1)*lazyTree[i]
                lazyTree[2*i+2]=(r-l+1)*lazyTree[i]
                lazyTree[i]=0
        if r<start or l>end or l>r:
            return
        if start<=l and end>=r:
            segmentTree[i]+=(r-l+1)*val
            if l!=r:
                lazyTree[2*i+1]+=val
                lazyTree[2*i+2]+=val
            return
        mid=l+(r-l)//2
        updateSegmentTree(start,end,2*i+1,l,mid,val,segmentTree,lazyTree)
        updateSegmentTree(start,end,2*i+2,mid+1,r,val,segmentTree,lazyTree)
        segmentTree[i]=segmentTree[2*i+1] +segmentTree[2*i+2]
    updateSegmentTree(start,end,0,0,n-1,val,segmentTree,lazyTree)
    return segmentTree


def splitNum(num):
    num=str(num)
    a=[]
    for i in range(len(num)):
        a.append(num[i])
    a.sort()
    num1=''
    num2=''
    for i in range(len(a)):
        if i%2==0:
            num2+=a[i]
        else:
            num1+=a[i]
    return int(num1)+int(num2)

def minimumAddedInteger(nums1, nums2):
        nums1.sort()
        nums2.sort()
        minValue=float("inf")
        min2=min(nums2)
        min1=min(nums1)
        max1=max(nums1)
        max2=max(nums2)
        print(max2,max1,min1,min2)
        
print(minimumAddedInteger([9,4,3,9,4], nums2 = [7,8,8]))

