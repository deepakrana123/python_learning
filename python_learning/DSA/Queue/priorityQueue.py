class PirorityQueue:
    def __init__(self):
        self.queue = []

    def push(self, data, priority):
        index = 0
        while index < len(self.queue) and self.queue[index][1] <= priority:
            index += 1
        self.queue.insert(index, (data, priority))

    def is_Empty(self):
        return len(self.queue)

    def popByPriority(self, priority):
        index = 0
        while index < len(self.queue) and self.queue[index][1] <= priority:
            index += 1
        self.queue.pop(index)

    def pop(self):
        if self.is_Empty():
            raise IndexError("Qeueue is empty")
        self.queue.pop(0)[0]

    def size(self):
        return len(self.queue)


class Node:
    def __init__(self, item=None, priority=None, next=None):
        self.item = item
        self.next = next
        self.priority = priority


class PirorityQueueLinkedList:
    def __init__(self):
        self.start = None
        self.item_count = 0

    def push(self, data, priority):
        n = Node(data, priority)
        if not self.start or priority < self.start.priority:
            n.next = self.start
            self.start = n
        else:
            temp = self.start
            while temp.next and temp.next.priority <= priority:
                temp = temp.next
            n.next = temp.next
            temp.next = n
        self.item_count += 1

    def isEmpty(self):
        return self.start == None

    def pop(self):
        if self.isEmpty():
            raise IndexError("Priority queue is empty")
        data = self.start.item
        self.start = self.start.next
        self.item_count -= 1
        return data

    def size(self):
        return self.item_count
