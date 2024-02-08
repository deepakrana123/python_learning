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
    def insert_after_Poiiint(self,temp,data):
        if temp is not None:
            n=Node(data,temp,temp.next)
            if temp.next is not None:
                temp.next.prev=n
            temp.next=n
    def printAll(self):
        temp=self.start
        while temp.next!=None:
            print(temp.val)
            temp=temp.next
    def delete_At_First(self):
        if self.start !=None:
            self.start=self.start.next
            if self.start !=None:
                self.start.prev=None
    def delete_At_Last(self):
        if self.start is None:
            pass
        elif self.start.next is None:
            self.start=None
        else:
            temp=self.start
            while temp!=None and temp.next!=None:
                temp=temp.next
            temp.prev.next=None
        
    def delete_At_Point(self,data):
        if self.start is None:
            pass
        else:
            temp=self.start
            while temp!=None and temp.next!=None:
                if temp.item==data:
                    temp.next.prev=temp.prev
                    if temp.prev is not None:
                        temp.prev.next=temp.next
                    else:
                        self.start=temp.next
                    break
                temp=temp.next
    def __iter__(self):
        return DLLIerator(self.start)

class DLLIerator:
    def __init__(self,start):
        self.current=start
    def __iter__(self):
        return self
    def __next(self):
        if not self.current:
            raise StopIteration
        data=self.current.item
        self.current=self.current.next
        return data
                        
                    
                
                
        
        
        
            
        
        