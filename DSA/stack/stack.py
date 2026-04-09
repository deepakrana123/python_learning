class Stack:
    def __init__(self):
        self.items=[]
    def isEmpty(self):
        return len(self.items)==0
    
    def push(self,data):
        self.items.append(data)
    
    def peak(self):
        if not self.isEmpty():
            return self.items[-1]
        else:
            raise IndexError("Stack is Empty")
    
    def pop(self):
        if not self.isEmpty():
            return self.items.pop()
        else:
            raise IndexError("Stack is Empty")
    
    def size(self):
        return len(self.items)
    


class Stack(list):
    def isEmpty(self):
        return len(self)==0
    
    def push(self,data):
        self.append(data)
    
    def peak(self):
        return self[-1]
    
    def pop(self):
        if not self.isEmpty():
            # super helps to stop overiding if parent and child have same function name
            return super().pop()
        else:
            raise IndexError("Stack is Empty")
    
    def size(self):
        if not self.isEmpty():
            return len(self)
        else:
            raise IndexError("Stack is Empty")
    def insert(self,index,data):
        raise AttributeError("Bhai na kar yeh")
    
# s1=Stack()
# s1.insert()


class Node:
    def __init__(self,item=None,next=None):
        self.item=item
        self.next=next
        
class StackLinkedList:
    def __init__(self):
        self.top=None
        self.itemCount=0
    def isEmpty(self):
        return self.top==None
    def push(self,data):
        n=Node(data,self.top)
        self.top=n
        self.itemCount+=1
    def pop(self):
        if self.isEmpty():
            raise IndexError("Stack is empty could pop")
        else:
            data=self.top.item
            self.top=self.top.next
            self.itemCount-=1
            return data
    def peek(self):
        if self.isEmpty():
            raise IndexError("Stack is empty")
        return self.top.item
    def size(self):
        return self.itemCount
    

s1=StackLinkedList()
s1.push(10)
s1.push(11)
s1.push(13)
print("Total elements in the stack",s1.size(),s1.peek())
    
    

        
    
        
           

        