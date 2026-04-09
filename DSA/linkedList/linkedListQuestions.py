class Solution:
    def deleteNode(self, node):
        while node !=None and node.next!=None:
            node.val=node.next.val
            prev=node
            node=node.next
        prev.next=None
        
