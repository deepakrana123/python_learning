#graph representation
# adjancey matrix and adjancey list


class Solution:
    # def dfs(visited,trust,currNode):
    #     visited[currNode]=True
    #     for u,v in
    def findJudge(self, n: int, trust) -> int:
        self.result=-1
        self.graph={i:[] for i in range(1,n+1)}
        for u,v in trust:
            self.graph[u].append(v)
        print(self.graph)
        for item in self.graph:
            if(len(self.graph[item])==0):
                self.result=item
        
        for item in self.graph:
            if self.result not in  self.graph[item] and self.result!=item:
                return -1
        return self.result
a=Solution()
print(a.findJudge(3,[[1,3],[2,3]]))

        

        