# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def deleteMiddle(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if head.next==None or head==None:
            return None
        start=head
        fast=head
        prevSlow=None
        while fast !=None and fast.next !=None:
            prevSlow=start
            start=start.next
            fast=fast.next.next
        prevSlow.next=start.next
        return head
class Solution:
    def deleteNode(self, node):
        """
        :type node: ListNode
        :rtype: void Do not return anything, modify node in-place instead.
        """
        while node !=None and node.next!=None:
            node.val=node.next.val
            prev=node
            node=node.next
        prev.next=None