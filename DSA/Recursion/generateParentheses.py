def solve(curr,result,n):
    if curr==2*n:
        list1= "".join(str(x) for x in curr)
        if isValid(list1):
            result.append(list1)
        else:
            return
    curr.append("(")
    solve(curr,result,n)
    curr.pop()
    curr.append(")")
    solve(curr,result,n)
def generateParentheses(n):
    # if
    result=[]
    curr=[]
    solve(curr,result,n)
    return result

def isValid(str):
    stack=0
    for n in str:
        if n=='(':
            stack+=1
        else:
            stack-=1
    return stack==0
def backtrack(result,curr,open,close,n):
    if len(curr)==2*n:
        list1="".join(str(x) for x in curr)
        result.append(list1)
    if open<n:
        curr.append('(')
        self.backtrack(result,curr,open+1,close,n)
        curr.pop()
    elif close<open:
        curr.append(')')
        self.backtrack(result,curr,open,close+1,n)
        curr.pop()
def generate(n):
    result=[]
    open=0
    close=0
    curr=[]
    backtrack(result,curr,open,close,n)
    return result
        
def removeDuplicate(arr):
    a={}
    for num in arr:
        if num in a:
            a[num]+=1
        else:
            a[num]=1
    as1=[]
    for n in a:
        as1.append(n)
    print(as1) 
removeDuplicate([1,1,2,2,2,3,3])
def removeDuplicate1(arr):
    i=0
    for j in range(1,len(arr)):
        if arr[i]!=arr[j]:
            i+=1
            arr[i]=arr[j]
    return arr
b=removeDuplicate1([1,1,2,2,2,3,3])
print(b)
def rotate(nums, k):
    l=len(nums)-k
    a=[]
    for i in range(len(nums)-1,l-1,-1):
        a.append(nums[i])
    b=list(reversed(a))
    for i in range(l):
        nums[k+i]=nums[i]
    for i in range(k):
        nums[i]=b[i]
    print(b)
print(rotate([1,2,3,4,5,6,7],3))
        