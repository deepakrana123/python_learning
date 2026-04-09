
class Node:
    def __init__(self, x: int, next: 'Node' = None, random: 'Node' = None):
        self.val = int(x)
        self.next = next
        self.random = random


class Solution:
    def copyRandomList(self, head: 'Optional[Node]') -> 'Optional[Node]':
        map={}
        if head ==None:
            return None
        curr=head
        prev=Node()
        newHead=Node()
        
        while(curr!=None):
            temp=Node(curr.val) 
            map[curr]=temp
            if newHead==None:
                newHead=temp
                prev=newHead
            else:
                prev.next=temp
                prev=temp
            curr=curr.next
        
        curr=head
        newCurr=newHead
        while curr!=None:
            if curr.random==None:
                newCurr.random=None
            else:
                newCurr.random=map[curr.random]
            curr=curr.next
            newCurr=newCurr.next
        return newHead
        
        
        