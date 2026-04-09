class Node:
    def __init__(self,item=None,next=None):
        self.item=item
        self.next=next
class CLL:
    def __init__(self,last=None):
        self.last=last
    def isEmpty(self):
        if self.last==None:
            return True
        else:
            return False
    def insert_At_Start(self,data):
        n=Node(data)
        if self.isEmpty():
            n.next=n
            self.last=n
        else:
            n.next=self.last.next
            self.last.next=n
    def insert_At_Last(self,data):
        n=Node(data)
        if self.isEmpty():
            n.next=n
            self.last=n
        else:
            n.next=self.last.next
            self.last.next=n
            self.last=n
    def search(self,data):
        if self.isEmpty():
            return None
        temp=self.last.next
        while temp!=self.last:
            if temp.item==data:
                return True
            temp=temp.next
        if temp.item==data:
            return True
        return False
    def insert_After(self,temp,data):
        if temp!=None:
            n=Node(data,temp.next)
            temp.next=n
            if temp==self.last:
                self.last=n
    def print_list(self):
        if self.isEmpty():
            return None
        if self.last==None:
            return None
        temp=self.last.next
        while temp!=self.last:
            print(temp.item,end='')
            temp=temp.next
        print(temp.item)
    def delete_First(self):
        if self.isEmpty():
            return None
        else:
            if self.last.next==self.last:
                self.last=None
            else:
                self.last.next=self.last.next.next
    def delete_Last(self):
        if self.isEmpty():
            return None
        if self.last==None:
            return None
        temp=self.last.next
        while temp!=self.last:
            temp=temp.next
        temp.next=self.last.next
        self.last=temp
    def delete_item(self,data):
        if not self.isEmpty():
            if self.last.next==self.last:
                if self.last.item==data:
                    self.last=None
            else:
                if self.last.next.item==data:
                    self.delete_First()
                else:
                    temp=self.last.next
                    while temp!=self.last:
                        if temp.next==self.last:
                            if self.last.item==data:
                                self.delete_Last()
                            break
                        if temp.next.item==data:
                            temp.next=temp.next.next
                            break
                        temp=temp.next
            return None
        def __iter__(self):
            if self.last==None:
                return CLLIerator(None)
            return CLLIerator(self.last.next)

class CLLIerator:
    def __init__(self,start):
        self.current=start
        self.first=start
    def __iter__(self):
        return self
    def __next(self):
        if self.current==None:
            raise StopIteration
        data=self.current.item
        self.current=self.current.next
        if self.current==self.first:
            raise StopIteration
        return data
          
                        
                
        
        
        
        
        
    
            
            
            
        
            
        