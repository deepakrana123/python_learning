import collections 
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
class Solution:
    def swapNodes(self, head: Optional[ListNode], k: int) -> Optional[ListNode]:
        linked_list=collections.deque()
        current = head
        while current:
            linked_list.append(current)
            current = current.next
        length_of_linked_list = len(linked_list)
        k1=k
        node1=head
        while k1>1:
            node1=node1.next
            k1=k1-1
        k2=length_of_linked_list-k+1
        node2=head
        while k2>1:
            node2=node2.next
            k2=k2-1
        temp=node1.value
        node1.value=node2.value
        node2.value=temp
        return head
class Solution:
    def swapPairs(self, head: Optional[ListNode]) -> Optional[ListNode]:
        # A=head
        # B=head.next
        # C=head.next.next
        temp=head.next
        head.next=self.swapPairs(head.next.next)
        temp.next=head
        return temp
class Solution:
    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        linked_list1=collections.deque()
        current = l1
        while current:
            linked_list1.append(current)
            current = current.next
        linked_list1.reverse()
        linked_list2=collections.deque()
        current = l2
        while current:
            linked_list2.append(current)
            current = current.next
        linked_list2.reverse()
        l1=linked_list1
        l2=linked_list2
        
    
            
