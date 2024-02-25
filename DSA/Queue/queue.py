class Queue:
    def __init__(self):
        self.items = []
        self.front = None
        self.rear = None
    def is_empty(self):
        # if self.front==None and self.rear==None:
        #     return True
        # else:
        #     return False
        return len(self.items) == 0
    def enqueue(self, data):
        self.items.append(data)
        self.rear += 1
    def dequeue(self):
        if not self.is_empty():
            self.items.pop(0)
            self.front = 0
        else:
            raise IndexError("Queue underflow")
    def get_enqueue(self):
        # return self.items[self.rear]
        if not self.is_empty():
            return self.items[-1]
        else:
            raise IndexError("Queue underflow")
    def get_dequeue(self):
        if not self.is_empty():
            return self.items[0]
        else:
            raise IndexError("Queue underflow")
    def get_Size(self):
        return len(self.items)
q1 = Queue()
try:
    print(q1.get_enqueue())
except IndexError as e:
    print(e.args[0])

q1.enqueue(20)
q1.enqueue(21)
q1.enqueue(22)
q1.enqueue(23)
q1.enqueue(24)
print("Front=", q1.enqueue())
print("Reaer=", q1.get_enqueue())

