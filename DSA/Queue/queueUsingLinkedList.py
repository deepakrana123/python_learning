class Node:
    def __init__(self,value=None,next=None):
        self.value=value
        self.next=next

class QueueUsingLinkedList:
    def __init__(self):
        self.front=None
        self.rear=None
        self.itemCount=0
    def isEmpty(self):
        if self.front==None or self.rear==None or self.itemCount==0:
            return True
        else:
            return False
    def enqueue(self,item):
        n=Node(item,None)
        if self.isEmpty():
            self.front=n
        else:
            self.rear.next=n
        self.rear=n
        self.itemCount+=1
    def dequeue(self):
        if self.isEmpty():
            raise IndexError("Empty Queue")
        elif self.front==self.rear:
            self.front=None
            self.rear=None
            self.itemCount-=1
        else:
            self.front=self.front.next
    def get_rear(self):
        if self.isEmpty():
            raise IndexError("No data in the queue")
        else:
            return self.rear.item
    def get_front(self):
        if self.isEmpty():
            raise IndexError("No data in the queue")
        else:
            return self.front.item
    def getSize(self):
        return self.itemCount
        
        
        
            
        
        
        
        