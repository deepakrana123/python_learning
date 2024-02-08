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
            return super().pop()
        else:
            raise IndexError("Stack is Empty")
    
    def size(self):
        if not self.isEmpty():
            return len(self)
        else:
            raise IndexError("Stack is Empty")
        
           

        