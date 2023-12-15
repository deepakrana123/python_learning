from collections import deque
class Solution:
    def minimumTime(self, n: int, relations: List[List[int]], time: List[int]) -> int:
        adj={i:[] for i in range(n)}
        queue = deque()
        indegree=[0 for _ in range(n)]
        for u in range(len(relations)):
            a=relations[u][0]-1
            b=relations[u][1]-1
            adj[a].append(b)
            indegree[b]+=1
        maxTime=[0]*(n)
        for i in range(len(indegree)):
            if(indegree[i]==0):
                queue.append(i)

        while(len(queue)!=0):
            c=queue.popleft()
            for u in adj[c]:
                maxTime[c]=max(maxTime[c],maxTime[u]+time[c])
                indegree[c]=indegree[c]-1
                if(indegree[c]==0):
                    queue.append(c)
        return max(maxTime)

