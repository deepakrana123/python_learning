# singly link list
"""singly link list"""
print("try your best to become best")

class Node:
    def __init__(self,item,next):
        self.item=item
        self.next=next

class SinglyLinkList:
    def __init__(self,start=None):
        self.start=start
    def isEmpty(self):
        return self.start==None


#driver code
myList=SinglyLinkList(0)
        