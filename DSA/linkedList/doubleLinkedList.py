class Node:
    def __init__(self,item=None,prev=None,next=None):
        self.item=item
        self.next=next
        self.prev=prev

class DoubleyLinkedList:
    def __init__(self):
        self.start=None
    def isEmpty(self):
        if self.start==None:
            return True
    def addInitally(self,value):
        n=Node()
        n.item=value
        n.prev=None
        n.next=self.start
        if not self.isEmpty():
            self.start.prev=n
        self.start=n
    def addLast(self,value):
        n=Node()
        n.item=value
        n.next=None
        temp=self.start
        while temp.next !=None and temp!=None:
            temp=temp.next
        n.prev=temp
        if temp==None:
            self.start=n
        else:temp.next=n
    def search(self,data):
        temp=self.start
        if temp is not None:
            if temp.item==data:
                return temp
            temp=temp.next
        return None
    def insert_after(self,temp,data):
        if temp is not None:
            n=Node(data,temp.next,)
            
        
            
        
        