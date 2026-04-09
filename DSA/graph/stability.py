class Disjoint:
    def __init__(self):
        self.rank=[0]*26
        self.parent=[i for i in range(26)]

    def find(self,x):
        if self.parent[x]==x:
            return x
        self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    def Union(self,x,y):
        root_x=self.find(x)
        root_y=self.find(y)
        if root_x==root_y:
            return False
        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
        elif self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
        else:
            self.parent[root_y] = root_x
            self.rank[root_x] += 1
        
class Solution:
    def equationsPossible(self, equations) -> bool:
        disjoint=Disjoint()
        nq=[]
        n=len(equations)
        for i in range(n):
            if(equations[i][1]=='!'):
                if(equations[i][0]==equations[i][-1]):
                    return False
                else:
                    nq.append(equations[i])
            else:
                disjoint.Union(ord(equations[i][0])-97,ord(equations[i][-1])-97)
        
        for i in range(len(nq)):
            x=ord(nq[i][0])-97
            y=ord(nq[i][-1])-97
            print(x,y,disjoint.find(x))
            if disjoint.find(x) == disjoint.find(y):
                return False
        return True

sol=Solution()
result=sol.equationsPossible(["c==c","b==d","x!=z"])
print(result)