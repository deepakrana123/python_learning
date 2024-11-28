from collections import deque
import heapq

class DailyRevision:
    def slidingPuzzle(self, board):
        start=""
        target="123450"
        for i in range(len(board)):
            for j in range(len(board[0])):
                start+=board[i][j]
        queue=deque()
        queue.append(str)
        adj={i:{} for i in range(len(board[0]))}
        adj[0]={1,3}
        adj[1]={0,2,4}
        adj[2]={1,5}
        adj[3]={0,4}
        adj[4]={1,3,5}
        adj[5]={2,4}
        visited=set()
        visited.add(start)
        level=0
        while queue:
            for _ in range(len(queue)):
                curr=queue.popleft()
                if curr==target:
                    return level
                indexOfZero=curr.index(0)
                for swapIndex in adj[indexOfZero]:
                    newState=curr
                    newState[indexOfZero]=newState[swapIndex]
                    if newState not in visited:
                        visited.add(newState)
                        queue.append(newState)
            level+=1
        return -1
    def findChampion(self, n: int, edges) -> int:
        indegree=[0]*n
        for u,v in edges:
            indegree[v]+=1
        minA=float("inf")
        minIndex=0
        for i in range(len(indegree)):
            if minA==indegree[i]:
                minIndex=-1
            if minA>indegree[i]:
                minA=indegree[i]
                minIndex=i
        return minIndex if minIndex!=-1 else -1
    def rotateMatrix90degree(self,a):
        for i in range(len(a[0])):
            for j in range(len(a)):
                a[i][j],a[j][i]=a[j][i],a[i][j]
        for i in range(len(a)):
            a.reverse()
        return a
    def rotateTheBox(self, box):
        result=[[0 for _ in range(len(box))] for _ in range(len(box[0]))]
        for i in range(len(box[0])):
            for j in range(len(box)):
                result[i][j]=box[j][i]
        for i in range(len(result)):
            result.reverse()
    def maxMatrixSum(self, matrix):
        sums=0
        countNegative=0
        minImunNegNumber=float("inf")
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                if matrix[i][j]<0:
                    countNegative+=1
                    minImunNegNumber=min(minImunNegNumber,abs(matrix[i][j]))
                sums+=abs(matrix[i][j])
        return sums if countNegative%2==0 else sums - 2*minImunNegNumber
    def minMutation(self, startGene, endGene, bank):
        queue=deque()
        quickAccess=set(bank)
        queue.append(startGene)
        visited=set()
        visited.add(startGene)
        abc=['A','C','G','T']
        level=0
        while queue:
            n=len(queue)
            while n:
                curr=queue.popleft()
                if curr == endGene:
                    return level
                for j in range(len(abc)):
                    for i in range(len(curr)):
                            aab=list(curr)
                            aab[i]=abc[j]
                            newNeighbout="".join(aab)
                            if newNeighbout not in visited and newNeighbout in quickAccess:
                                visited.add(newNeighbout)
                                queue.append(newNeighbout)
                n-=1
            level+=1
        return -1
    def ladderLength(self, beginWord, endWord, wordList):
        quickAccess=set(wordList)
        queue=deque()
        queue.append(beginWord)
        visited=set()
        visited.add(beginWord)
        level=0
        abc=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
        while queue:
            n=len(queue)
            while n:
                curr=queue.popleft()
                if curr==endWord:
                    return level
                for i in range(len(abc)):
                    for j in range(len(curr)):
                        newCurr=list(curr)
                        newCurr[j]=abc[i]
                        newAppendCurr="".join(newCurr)
                        if newAppendCurr not in visited and newAppendCurr in  quickAccess:
                            visited.add(newAppendCurr)
                            queue.append(newAppendCurr)   
                n-=1
            level+=1
        return level 
    def nearestExit(self, maze, entrance):
        m=len(maze)
        n=len(maze[0])
        queue=deque()
        dir=[[-1,0],[0,-1],[1,0],[0,1]]
        queue.append((entrance[0], entrance[1]))
        maze[entrance[0]][entrance[1]]='+'
        step=0
        while queue:
            # n=len(queue)
            for _ in range(len(queue)):
                newRow,newCol = queue.popleft()
                if((newRow!=entrance[0] or newCol!=entrance[1]) and (newRow==0 or newRow==m-1 or newCol==0 or newCol==n-1)):
                    return step
                for dirs in dir:
                    newRowX=newRow + dirs[0]
                    newRowY=newCol + dirs[1]
                    if  0<=newRowX < m and 0<= newRowY < n and maze[newRowX][newRowY] == '.':
                        queue.append((newRowX,newRowY))
                        maze[newRowX][newRowY]='+'
                # n-=1
            step+=1
        return -1
    def dfs(self,adj,color,index):
        color[index]=1
        queue=deque()
        queue.append(index)
        while queue:
            print(queue,adj)
            curr=queue.popleft()
            for v in adj[curr]:
                if color[v]==color[curr]:
                    return False
                if color[v] == -1:
                    queue.append(v)
                    color[v] = 1-color[curr]
        return True
    # def possibleBipartition(self, n: int, dislikes):
    #     adj={i:[] for i in range(1,n+1)}
    #     for u,v in dislikes:
    #         adj[u].append(v)
    #         adj[v].append(u)
    #     color=[-1]*(n+1)
    #     for i in range(1,n+1):
    #         if color[i]==-1 and self.dfs(adj,color,i) == False:
    #             return False
    #     return True
    # def sumOfDistancesInTree(self, n: int, edges):
    #     adj={i:[] for i in range(n)}
    #     for u,v in edges:
    #         adj[u].append(v)
    #         adj[v].append(u)
    def bfs(self,adj,n):
        queue=deque()
        queue.append(0)
        visited=set()
        visited.add(0)
        level=0
        while queue:
            for _ in range(len(queue)):
                curr=queue.popleft()
                if curr==n-1:
                    return level
                for v in adj[curr]:
                    if v not in visited:
                        visited.add(v)
                        queue.append(v)
            level+=1
        return -1
    def dijistra(self,adj,n):
        result=[float("inf")]*n
        result[0]=0
        queue=[(0,0)]
        while queue:
            a= heapq.heappop(queue)
            dist,node=a
            if node==n-1:
                return result[n-1]
            for v in adj[node]:
                vNode=v[0]
                vDist=v[1]
                if dist+vDist<result[vNode]:
                    result[vNode]=dist+vDist
                    heapq.heappush(queue,(dist+vDist,vNode))
        return result[n-1]
    def shortestDistanceAfterQueries(self, n: int, queries):
        adj={i:[] for i in range(n)}
        # for i in range(n-1):
        #     adj[i].append(i+1)
        # result=[0]*len(queries)
        # for i in range(len(queries)):
        #     u,v=queries[i]
        #     adj[u].append(v)
        #     result[i]=self.bfs(adj,n)
        # return result
        for i in range(n-1):
            adj[i].append((i+1,1))
        result=[0]*len(queries)
        for i in range(len(queries)):
            u,v=queries[i]
            adj[u].append((v,1))
            result[i]=self.dijistra(adj,n)
        return result
    def dfs1(self,adj,curr,parent,result):
        longest1=0
        longest2=0
        for child in adj[curr]:
            if child==parent:
                continue
            childdistance=self.dfs1(adj,child,curr,result)
            if longest2<childdistance:
                longest2=childdistance
            if  longest2>longest1:
                longest2=longest1
                longest1=childdistance
        koi_ek_accha=max(longest1,longest2)+1
        only_root=1
        neeche_hi_mil=max(longest2,longest1)
        result[0]=max(result[0],only_root,koi_ek_accha,neeche_hi_mil)
        return max(koi_ek_accha,only_root)
    def longestPath(self, parent, s):
        adj={i:[] for i in range(len(parent))}
        for i in range(1,len(parent)):
            u=i
            v=parent[i]
            adj[u].append(v)
            adj[v].append(u)
        result=[0]
        self.dfs1(adj,0,-1,result)
        return result[0]
    def smallestEquivalentString(self, s1, s2, baseStr):
        adj={i:[] for i in range(len(s1))}
        for i in range(len(s1)):
            adj[s1[i]].append(s2[i])
            adj[s2[i]].append(s1[i])
        result=""
        self.dfs3(adj,)
        
a=DailyRevision()
# print(a.maxMatrixSum([[1,-1],[-1,1]]))
# print(a.minMutation("AACCGGTT", endGene ="AACCGCTA", bank = ["AACCGGTA","AACCGCTA","AAACGGTA"]))
# print(a.ladderLength("hit", endWord = "cog", wordList = ["hot","dot","dog","lot","log"]))
# print(a.nearestExit([["+","+","+"],[".",".","."],["+","+","+"]], entrance = [1,0]))
# print(a.possibleBipartition( 3, dislikes = [[1,2],[1,3],[2,3]]))
# print(a.findChampion(4, edges = [[0,2],[1,3],[1,2]]))
# print(a.sumOfDistancesInTree(6, edges = [[0,1],[0,2],[2,3],[2,4],[2,5]]))
# print(a.shortestDistanceAfterQueries(4, queries = [[0,3],[0,2]]))
# print(a.longestPath(parent = [-1,0,0,1,1,2], s = "abacbe"))
print(a.smallestEquivalentString(s1 = "parker", s2 = "morris", baseStr = "parser"))
        
        
a=DailyRevision()

# print(a.rotateTheBox([["#",".","#"]]))



