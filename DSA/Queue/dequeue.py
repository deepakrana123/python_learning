class Deque:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return len(self.items) == 0

    def insert_Front(self, data):
        self.items.insert(0, data)

    def insert_rear(self, data):
        self.items.append(data)

    def delete_Front(self):
        if self.isEmpty():
            raise IndexError("Queue is empty could delete ")
        else:
            self.items.pop(0)

    def delete_rear(self):
        if self.isEmpty():
            raise IndexError("Queue is empty could delete ")
        else:
            self.items.pop()

    def get_front(self):
        if self.isEmpty():
            raise IndexError("Queue is empty could delete ")
        else:
            return self.items[0]

    def get_front(self):
        if self.isEmpty():
            raise IndexError("Queue is empty could delete ")
        else:
            return self.items[-1]

    def size(self):
        return len(self.items)
