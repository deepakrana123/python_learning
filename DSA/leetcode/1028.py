class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
def recoverFromPreorder(traversal):
    i=[0]
    depth=0
    n=len(traversal)
    def solve(i,depth,traversal,n):
        if i[0]>=n:
            return None
        j=0
        while j<n and traversal[j]=='_':
            j+=1
        dash=j-i[0]
        if dash!=depth:
            return None
        i[0]+=dash
        num=0
        while i[0]<n and traversal[i[0]].isdigit():
            num=num*10+int(traversal[i[0]])
            i[0]+=1
        root=TreeNode(num)
        root.left=solve(i,depth+1,traversal,n)
        root.right=solve(i,depth+1,traversal,n)
        return root

    return solve(i,depth,traversal,n)
        