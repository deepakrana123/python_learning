class Solution:
    def dfs(self,adj,visited,index):
        visited[index]=True
        for u in adj[index]:
            if visited[u]==False:
                self.dfs(adj,visited,u)
    def isSimilar(self,str1,str2):
        m=len(str1)
        diff=0
        for i in range(len(str1)):
            if str1[i]!=str2[i]:
                diff+=1
        return True if diff==2 or diff==0 else False
    def numSimilarGroups(self, strs: List[str]) -> int:
        a={i:[] for i in range(len(strs))}
        for i in range(len(strs)):
            for j in range(i+1,len(strs)):
                if self.isSimilar(strs[i],strs[j]):
                    a[i].append(j)
                    a[j].append(i)
        visited=[False]*len(a)
        count=0
        for i in range(len(a)):
            if not visited[i]:
                self.dfs(a,visited,i)
                count=count+1
        return count

# by dsu