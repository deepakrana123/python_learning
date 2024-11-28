class Tree:
    def inorderTraversal(self,root):
        if root==None:
            return 
        stack=[]
        def inorder(root,stack):
            self.inorderTraversal(root.left)
            stack.append(root.val)
            self.inorderTraversal(root.right)
        inorder(root,stack)
        return stack
    def isSymmtrix(self,root):
       if root==None:
        return

        def isMirror(leftNode,rightNode):
            if leftNode is None and rightNode is None:
                return True
            if leftNode is None or rightNode is None:
                return False
            return leftNode.data==rightNode.data and isMirror(leftNode.right,rightNode.left) and isMirror(leftNode.left,rightNode.right)
        isMirror(root.left,root.right)