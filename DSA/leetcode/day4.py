def solve(i , open ,s,dp):
    if i==len(s):
        return open==0
    isValid=False
    if dp[i][open]!=-1:
        return dp[i][open]
    if s[i]=='(':
        isValid=solve(i+1,open+1,s,dp)
    elif s[i]=='*':
        isValid  = isValid or solve(i+1,open+1,s,dp)
        if open>0:
           isValid=isValid or solve(i+1,open-1,s,dp)
        isValid = isValid or solve(i+1,open,s,dp)
    else: 
        if open>0:
            isValid= solve(i+1,open-1,s,dp)
    dp[i][open]=isValid
    return dp[i][open]
def checkValidString(s):
    dp=[[-1 for i in range(len(s)+1)] for j in range(len(s)+1)]
    return solve(0,0,s,dp)

def checkValidStr(s):
    dp=[[False for i in range(len(s)+1)] for j in range(len(s)+1)]
    dp[len(s)][0]=True
    for index in range(len(s)-1,-1,-1):
        for open in range(len(s)):
            isValid=False
            if s[index]=="*":
                isValid= isValid or dp[index+1][open+1]
                isValid=isValid or dp[index+1][open]
                if open>0:isValid=isValid or dp[index+1][open-1]
            elif s[index]=='(':
                isValid=isValid or dp[index+1][open+1]
            elif open>0 and s[index]==')':
                isValid= isValid or dp[index+1][open-1]
            dp[index][open]=isValid
    return dp[0][0]
print(checkValidStr("()"))
def dfs(u,result,prev,m):
    result.append(u)
    for v in m[u]:
        if v!=prev:
            dfs(v,result,u,m)
    return result
def restoreArray(adjacentPairs):
    max_index = max(max(pair) for pair in adjacentPairs)
    min_index = min(min(pair) for pair in adjacentPairs)
    m = {i: [] for i in range(min_index,max_index+1)}
    for i in range(len(adjacentPairs)):
        u=adjacentPairs[i][0]
        v=adjacentPairs[i][1]
        m[u].append(v)
        m[v].append(u)
    result=[]
    start=0
    for key in m:
        if len(m[key])==1:
            start=key
            break
    return dfs(start,result,float("-inf"),m)
            
    
print(restoreArray([[4,-2],[1,4],[-3,1]]))
print(restoreArray([[2,1],[3,4],[3,2]]))

def equalPairs(grid):
    m={}
    count=0
    for row in range(len(grid)):
        a=tuple(grid[row])
        if a in m:
            m[a]+=1
        else:
            m[a]=1
    for col in range(len(grid[0])):
        temp=[]
        for r in range(len(grid)):
            temp.append(grid[r][col])
        count += m.get(tuple(temp), 0)
    return count
print(equalPairs([[3,1,2,2],[1,4,4,5],[2,4,2,2],[2,4,2,2]]))             
            
    


        
    