class Solution:
    def plaindrome(self,s,i,j):
        while i < j:
            if s[i] != s[j]:
                return False
            i += 1
            j -= 1
        return True
    def solve(self,s,index,jndex):
        if index>=jndex:
            return 0
        if self.plaindrome(s,index,jndex):
            return 0
        result=float("inf")
        for k in range(index,jndex):
            temp=1+self.solve(s,index,k)+self.solve(s,k+1,jndex)
            result=min(result,temp)
        return result

    def minCut(self, s: str) -> int:
        return self.solve(s,0,len(s)-1)
a=Solution()
print(a.minCut("aab"))