import math 
def isPossible(target,points,m):
    moves=0
    advanceMoves=0
    normalMoves=0
    for i in range(len(points)):
        gamesPoints=points[i]
        games=math.ceil(target/gamesPoints)
        if advanceMoves>=games:
            advanceMoves=0
            normalMoves+=1
        else:
            pointsAreadyCovered = advanceMoves*gamesPoints
            games = math.ceil((target-pointsAreadyCovered)/gamesPoints)
            moves+=2*games-1
            advanceMoves = max(games-1,0)
            moves+=normalMoves
            normalMoves = 0
    return moves<=m


def maxScore(points, m):
    start=1
    end=pow(10,9)*pow(10,6)
    result=0
    while start<=end:
        mid=start + (end-start)//2
        if isPossible(mid,points,m):
            result=mid
            start=mid+1
        else:
            end=mid-1
    return result
print(maxScore([2,4], m = 3))