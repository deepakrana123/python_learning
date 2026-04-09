def countSteps(ringIndex,index,n):
    distance = abs(index-ringIndex)
    wraparound = abs(n-distance)
    return min(distance,wraparound)
def solve(ringIndex,keyIndex,ring,key,dp):
    if keyIndex >=len(key):
        return 0
    if dp[ringIndex][keyIndex]!=-1:
        return dp[ringIndex][keyIndex]
    result=float('-inf')
    for i in range(len(ring)):
        if ring[i]==key[keyIndex]:
            totalSteps=countSteps(ringIndex,i,len(ring))+1+solve(i,keyIndex+1,ring,key)
            result=min(totalSteps,result)
            dp[ringIndex][keyIndex]=result
    return dp[ringIndex][keyIndex]
            
def findRotateSteps(ring, key):
    dp = [[-1 for _ in range(len(ring) + 1)] for _ in range(len(ring))]
    return solve(0,0,ring,key,dp)
        