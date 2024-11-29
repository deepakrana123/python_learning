from collections import deque
import heapq

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
        def isMirror(leftNode,rightNode):
            if leftNode is None and rightNode is None:
                return True
            if leftNode is None or rightNode is None:
                return False
            return leftNode.data==rightNode.data and isMirror(leftNode.right,rightNode.left) and isMirror(leftNode.left,rightNode.right)
        if root==None:
            return
        isMirror(root.left,root.right)
    def treeTarversal(self,root,result,temp,targetSum,currentSum):
        if root==None:
            return
        currentSum+=root.val
        
        temp.append(root.val)
        if root.left==None and root.right==None:
            if currentSum==targetSum:
                result.append(temp)
                return
        self.treeTarversal(root.left,result,temp,targetSum,currentSum)
        self.treeTarversal(root.right,result,temp,targetSum,currentSum)
        
        # newStr=str(root.val) + newStr
        # if root.left==None and root.right==None:
        #     result.append(newStr)
        #     return
        # self.treeTarversal(root.left,result,newStr)
        # self.treeTarversal(root.right,result,newStr)
    def binaryTreePaths(self, root,targetSum ):
        result=[]
        temp=[]
        return self.treeTarversal(root,result,temp,targetSum,currentSum=0)
    def treeTarversal1(self,root,result):
        if root==None:
            return      
        self.treeTarversal1(root.left,result,True)
        self.treeTarversal1(root.right,result,False)

        result[0]=result[0]+root.val.left

    def sumOfLeftLeaves(self, root):
        result=[0]
        self.treeTarversal1(root,result)
        return result[0]
    def isValidBST(self, root):
        
        def dfs(root,mins=float("-inf") ,maxs=float('inf')):
            if root ==None:
                return True
            if root.value>mins or root.value < maxs:
                return dfs(root.left,root.value,maxs) or dfs(root.right,mins,root.value)
            else:
                return False
         
        return dfs(root,mins=float("-inf") ,maxs=float('inf'))
    def levelOrder(self, root):
        queue=[]
        queue.append(root)
        result=[]
        current_level=[]
        # while queue:
        #     current_node=queue.pop()
        #     if current_node is not None:
        #         result.append(current_level)
        #         current_level=[]
        #         if len(queue)==0:
        #             break
        #     else:
        #         current_level.append(current_node.val)
        #         if current_node.left is not None:
        #             queue.append(current_node.left)
        #         if current_node.right is not None:
        #             queue.append(current_node.right)
        # return result
        while queue:
            current_level=[]
            for _ in range(len(queue)):
                current_node=queue.pop()
                current_level.append(current_node.val)
                if current_node.left is not None:
                    queue.append(current_node.left)
                if current_node.right is not None:
                    queue.append(current_node.right)
            result.append(current_level)
        return result
    def zigzagLevelOrder(self, root):
        queue=[]
        queue.append(root)
        result=[]
        current_level=[]
        level=0
        while queue:
            current_level=[]
            for _ in range(len(queue)):
                current_node=queue.pop()
                current_level.append(current_node.val)
                if current_node.left is not None:
                    queue.append(current_node.left)
                if current_node.right is not None:
                    queue.append(current_node.right)
            if level%2!=0:
                result.append(current_level[::-1])
            else:
                result.append(current_level)
            level+=1
        return result
    def kthSmallest(self, root, k):
        result=[]
        stack=[]
        current=root
        while current or stack:
            while current:
                stack.append(current)
                current=current.left
            current=stack.pop()
            heapq.heappush(result,current.val)
            while k>0:
                a= heapq.heappop(result)
                k-=1
            current=current.right
        return result[0]


        

        
        
                


        
        
        