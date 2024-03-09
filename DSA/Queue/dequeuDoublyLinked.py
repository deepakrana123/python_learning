class Node:
    def __init__(self, item=None, prev=None, next=None):
        self.prev = prev
        self.next = next
        self.item = item


class Deque:
    def __init__(self):
        self.front = None
        self.rear = None
        self.itemCount = 0

    def isEmpty(self):
        if self.front == None or self.rear == None or self.itemCount == 0:
            return True
        else:
            return False

    def insert_Front(self, data):
        n = Node(data, None, self.front)
        if self.isEmpty():
            self.rear = n
        else:
            self.front.prev = n
        self.front = n
        self.itemCount += 1

    def insert_rear(self, data):
        n = Node(data, self.rear, None)
        if self.isEmpty():
            self.front = n
        else:
            self.rear.next = n
        self.rear = n
        self.itemCount += 1

    def delete_Front(self):
        if self.isEmpty():
            raise IndexError("Qeueue is empty")
        elif self.front == self.rear:
            self.front = None
            self.rear = None
        else:
            self.front = self.front.next
            self.front.prev = None
        self.itemCount -= 1

    def delete_Rear(self):
        if self.isEmpty():
            raise IndexError("Qeueue is empty")
        elif self.front == self.rear:
            self.front = None
            self.rear = None
        else:
            self.rear = self.rear.prev
            self.rear.next = None
        self.itemCount -= 1

    def get_Front(self):
        if self.isEmpty():
            raise IndexError("Qeueue is empty")
        else:
            return self.front.item

    def get_Rear(self):
        if self.isEmpty():
            raise IndexError("Qeueue is empty")
        else:
            return self.rear.item

    def isSize(self):
        return self.itemCount
    