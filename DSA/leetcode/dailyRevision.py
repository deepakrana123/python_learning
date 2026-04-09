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
    # def smallestEquivalentString(self, s1, s2, baseStr):
    #     adj={i:[] for i in range(len(s1))}
    #     for i in range(len(s1)):
    #         adj[s1[i]].append(s2[i])
    #         adj[s2[i]].append(s1[i])
    #     result=""
    #     self.dfs3(adj,)
    def minimumObstacles(self, grid):
        m=len(grid)
        n=len(grid[0])
        queue=[(0,(0,0))]
        dirs=[(-1,0),(1,0),(0,-1),(0,1)]
        result=[[float("inf") for _ in range(n)] for _ in range(m)]
        result[0][0]=0
        while queue:
            a= heapq.heappop(queue)
            weight,edges=a
            u,v=edges
            for d in dirs:
                newX=u + d[0]
                newY=v + d[1]
                if(newX < 0 or newX >=m or newY<0 or newY >=n ):
                    continue 
                currWiehgt = 1 if grid[newX][newY]==1 else 0
                if weight + currWiehgt< result[newX][newY]:
                    result[newX][newY]=weight+ currWiehgt
                    heapq.heappush(queue,(weight+ currWiehgt,(newX,newY)))
        return result[m-1][n-1] if result[m-1][n-1]!=float("inf") else -1
    def checkIfExist(self, arr):
        d=set()
        for value in arr:
            if value*2 in d or value/2 in d:
                return True
            d.add(value)
        return False
    def isPrefixOfWord(self, sentence, searchWord):
        a=sentence.split(' ')
        for i in range(len(a)):
            word=a[i][0:len(searchWord)]
         
            if word==searchWord:
                return i+1        
        return -1
    def dfsTree(self,root,targetSum,result,temp,sums):
        if root==None:
            return -1
        sums+=root.val
        path_count= 1 if sums==targetSum else 0
        path_count+=self.dfsTree(root.left,targetSum,result,temp,sums)
        path_count+=self.dfsTree(root.right,targetSum,result,temp,sums)
        return path_count
    def pathSum(self, root, targetSum):
        if root==None:
            return -1
        findoot=self.dfsTree(root,targetSum,[],[],0)
        findPathLeft=self.pathSum(root.left,targetSum)
        findPathRight=self.pathSum(root.right,targetSum)
        return findoot+findPathLeft+findPathRight
    def dfsFindSame(self,root,parent):
        if root==None:
            return 0
        path_count=1 if parent==root.val else 0
        path_count+=self.dfsFindSame(root.left,root.val)
        path_count+=self.dfsFindSame(root.right,root.val)
        return path_count
    # def longestUnivaluePath(self, root):
    #     if root==None:
    #         return 0
    #     a=self.dfsFindSame(root,-1)
    #     b=self.longestUnivaluePath(root.left)
    #     c=self.longestUnivaluePath(root.right)
    #     return a+b+c
        

class Solution:
    def find(self,x):
        if x!=self.parent[x]:
            self.parent[x]=self.find(self.parent[x])
        return self.parent[x]
    def Union(self,x,y):
        parent_x=self.find(x)
        parent_y=self.find(y)
        if parent_x!=parent_y:
            if self.rank[parent_x]>self.rank[parent_y]:
                self.parent[parent_y]=parent_x
            elif self.rank[parent_x]<self.rank[parent_y]:
                self.parent[parent_x]=parent_y
            else:
                self.parent[parent_x]=parent_y
                self.rank[parent_y]+=1
    def numberOfGoodPaths(self, vals, edges):
        n=len(vals)
        self.rank=[1]*n
        self.parent=[i for i in range(n)]
        adj={i:[] for i in range(n)}
        for u,v in edges:
            adj[u].append(v)
            adj[v].append(u)
        valueVsNode={}
        for i,value in enumerate(vals):
            if value not in valueVsNode:
                valueVsNode[value]=[]
            valueVsNode[value].append(i)
        result=n
        isActive=[False]*n
        for v in sorted(valueVsNode.keys()):
            nodes=valueVsNode[v]
            for currNodes in nodes:
                for adjNodes in adj[currNodes]:
                    if isActive[adjNodes]:
                        self.Union(adjNodes,currNodes)
                isActive[currNodes]=True
            parent_count = {}
            for node in nodes:
                root = self.find(node)
                if root not in parent_count:
                    parent_count[root] = 0
                parent_count[root] += 1
            for count in parent_count.values():
                result += count * (count - 1) // 2
        return result

a=DailyRevision()

b=Solution()

class Solution1:
    def canMakeSubsequence(self, str1: str, str2: str) -> bool:
        j=0
        i=0
        while i<len(str1) and j<len(str2):
          
            a=chr(ord(str1[i])-25) if str1[i]=='z' else chr(ord(str1[i])+1)
            if  (str1[i]==str2[j] or a==str2[j]):
                j+=1
            i+=1
        return j==len(str2)
    def find_parent(self,  i):
        if self.parent[i] == i:
            return i
        self.parent[i] = self.find_parent(self.parent[i])
        return self.parent[i]

    def union(self, x, y):
        xroot = self.find_parent( x)
        yroot = self.find_parent( y)

        if self.rank[xroot] < self.rank[yroot]:
            self.parent[xroot] = yroot
        elif self.rank[xroot] > self.rank[yroot]:
            self.parent[yroot] = xroot
        else:
            self.parent[yroot] = xroot
            self.rank[xroot] += 1
    def krushkal(self,a,skip,add):
        self.parent=list(range(self.n))
        self.rank=[0]*self.n
        sum_weight=0
        if(add!=-1):
            u,v,w,index=add
            self.union(u,v)
            sum_weight+=w
        for edge in range(len(a)):
            u,v,w,index=a[edge]
            if skip!=-1 and  edge ==skip[3]:
                continue
            parent_u=self.find_parent(u)
            parent_v=self.find_parent(v)
            if parent_u!=parent_v:
                self.union(u,v)
                sum_weight+=w
        root = self.find_parent(0)
        for i in range(1, self.n):
            if self.find_parent(i) != root:
                return float('inf')
        return sum_weight
    def findCriticalAndPseudoCriticalEdges(self, n, edges):
        edges = [edge + [i] for i, edge in enumerate(edges)]
        edges.sort(key=lambda x: x[2])
        self.n=n
        mst_weight=self.krushkal(edges,-1,-1)
        pseudo=[]
        critical=[]
        for edge in edges:
            if self.krushkal(edges,edge,-1)>mst_weight:
                critical.append(edge[3])
            elif self.krushkal(edges,-1,edge)==mst_weight:
                pseudo.append(edge[3])
        
        return [critical,pseudo]


        
daily=Solution1()

print(daily.findCriticalAndPseudoCriticalEdges(n = 5, edges = [[0,1,1],[1,2,1],[2,3,2],[0,3,2],[0,4,3],[3,4,3],[1,4,6]]))
        
        
        



