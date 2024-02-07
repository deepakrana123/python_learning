class Node:
    def __init__(self,item=None,prev=None,next=None):
        self.item=item
        self.prev=prev
        self.next=next


class CDLL:
    def __init__(self,start):
        self.start=start
    
    def isEmpty(self):
        if self.start==None:
            return True
        else:
            return False
    def add_First(self,item):
        n=Node(item)
        if not self.isEmpty():
            n.next=self.start
            n.prev=self.start.prev
            self.start.prev.next=n
            self.start.prev=n
        else:
            n.next=n
            n.prev=n
        self.start=n
    
    def add_Last(self,item):
        n=Node(item)
        if not self.isEmpty():
            n.next=self.start
            n.prev=self.start.prev
            n.prev.next=n
            self.start.prev=n
        else:
            n.next=n
            n.prev=n
        self.start=n
    def search(self,item):
        temp=self.start
        if temp==None:
            return None
        if temp.item==item:
            return temp
        else:
            temp=temp.next
            
        while temp!=self.start:
            if temp.item==item:
                return temp
            temp=temp.next
        if temp.item==item:
            return temp
        return None
    def add_Item(self,item,data):
        if data is not None:
            n=Node(item)
            n.prev=data
            n.next=data.next
            data.next.prev=n
            data.next=n
    def printAll(self):
        temp=self.start
        if temp is not None:
            print(temp.item , end='')
            temp=temp.next
            while temp is not self.start:
                print(temp.item,end='')
                temp=temp.next
    def delete_First(self):
        if not self.isEmpty():
            if self.start.next==self.start:
                self.start=None
            else:
                self.start.prev.next=self.start.next
                self.start.next.prev=self.start.prev
                self.start=self.start.next
        else:
            self.start=None
    def delete_Last(self):
        if not self.isEmpty():
            if self.start.next==self.start:
                self.start=None
            else:
                self.start.prev.prev.next=self.start
                self.start.prev=self.start.prev.prev
                
            