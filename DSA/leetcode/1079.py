def numTilePossibilities(tiles):
    def solve(tiles,used,result,curr):
        result.add(str(curr))
        for i in range(len(tiles)):
            if used[i]:
                continue
            used[i]=True
            curr.append(tiles[i])
            solve(tiles,used,result,curr)
            used[i]=False
            curr.pop()
        
    n=len(tiles)
    used=[False]*n
    result=set()
    curr=[]
    solve(tiles,used,result,curr)
    return len(result)-1
print(numTilePossibilities("AAABBC"))
        