def findMaxFish(grid):
    m=len(grid)
    n=len(grid[0])
    dirs=[[-1,0],[1,0],[0,1],[0,-1]]
    result=0
    def maxFish(i,j): 
        if i<0 and j<0 and j>m and j>n and grid[i][j]==0:
            return 0
        fishCount=grid[i][j]
        grid[i][j]=0
        for x,y in dirs:
            fishCount+=maxFish(i+x,j+y)
        return fishCount
    for i in range(m):
        for j in range(n):
            if grid[i][j]>0:
                result=max(maxFish(i,j),result)
    return result

def findMaxFistDSU(grid):
    


        