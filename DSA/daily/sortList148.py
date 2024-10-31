class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
class Solution:
    def sortList(self, head):
        arr=[]
        temp=head
        while temp:
            arr.append(temp.val)
            temp=temp.next
        arr.sort()
        abc=ListNode()
        temp=abc
        for num in arr:
            a=ListNode(num)
            temp.next=a
            temp=temp.next
        return abc.next
a=Solution()
print(a.sortList([4,2,1,3]))