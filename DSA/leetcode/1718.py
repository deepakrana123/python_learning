def solve(i,n,result,used):
    if i>=len(result):
        return True
    if(result[i]!=-1):
        return solve(i+1,n,result,used)
    for num in range(n,0,-1):
        if used[num]:
            continue
        used[num]=True
        result[i]=num
        print(used,result)
        if num==1:
            if solve(i+1,n,result,used):
                return True
        else:
            k = result[i]+i
            if k<len(result) and result[k]==-1:
                result[k]=num
                if solve(i+1,n,result,used):
                    return True
                
                result[k]=-1
        used[num]=False
        result[i]=-1
    return False

def constructDistancedSequence(n):
    result = [-1]*(2*n-1)
    used = [False]*(n+1)
    solve(0,n,result,used)
    return result
print(constructDistancedSequence(3))