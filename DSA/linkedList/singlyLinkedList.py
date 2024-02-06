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
    def insert_at_First(self,value):
        node = Node(value,self.start)
        self.start=node
    def insert_at_last(self,value):
        node=Node(value,None)
        if not self.isEmpty():
            while self.start.next!=None:
                self.start=self.start.next
            self.start.next=node
        else:
            self.start=node
    def serach(self,value):
        temp=self.start
        while temp is not None:
            if temp==value:return temp
            temp=temp.next
        return None
            
    def insert_At_any_point(self,value,temp):
        if temp is not None:
            n=Node(value,temp.next)
            temp.next=n
    def print_list(self):
        temp=self.start
        while temp!=None and temp.next!=None:
            print(temp)
            temp=temp.next
    def delete_at_First(self):
        if self.start==None:return None
        else:
            self.start=self.start.next
    def delete_at_last(self):
        if self.start==None:return None
        elif self.start.next is None:
            return self.start
        else:
            temp=self.start
            while temp.next.next!=None:
                temp=temp.next
            temp.next=None
    def delete_At_any(self,temp):
        
        
        
        
            
            
        
        


#driver code
# myList=SinglyLinkList(0)
        