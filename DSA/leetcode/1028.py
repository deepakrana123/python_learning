class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
def recoverFromPreorder(traversal):
        i=0
        depth=0
        n=len(traversal)
        def solve(i,depth,traversal,n):
            if i>=n:
                return None
            j=0
            while j<n and traversal[j]=='_':
                j+=1
            dash=j-i
            if dash!=depth:
                return None
            i+=dash
            num=0
            while i<n and traversal[i].isdigit():
                num = num*10 + int(traversal[i])
                i+=1
            root=TreeNode(num)
            print(root,num,i,j)
            root.left = solve(i,depth+1,traversal,n)
            root.right = solve(i,depth+1,traversal,n)
            return root
        return solve(i,depth,traversal,n)
print(recoverFromPreorder("1-2--3--4-5--6--7"))
        