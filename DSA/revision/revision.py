def twoSum(nums, target):
    # for i in range(len(nums)):
    #     for j in range(i, len(nums)):
    #         if nums[i] + nums[j] == target:
    #             return [i, j]
    # return [-1, -1]
    # i = 0
    # j = len(nums) - 1
    # arr = [(num, idx) for idx, num in enumerate(nums)]
    # arr.sort()
    # while i < j:
    #     s = arr[i][0] + arr[j][0]
    #     if s == target:
    #         return [arr[i][1], arr[j][1]]
    #     elif s < target:
    #         i += 1
    #     elif s > target:
    #         j -= 1
    # return [-1, -1]
    dict = {}
    for i in range(len(nums)):
        value = target - nums[i]
        if value in dict:
            return [dict[value], i]
        dict[nums[i]] = i
    return [-1, -1]


def lengthOfLongestSubstring(s):
    # i = 0
    # j = 0
    # result = 0
    # dicts = {}
    # while j < len(s):
    #     dicts[s[j]] = dicts.get(s[j], 0) + 1
    #     if dicts[s[j]] > 1:
    #         while dicts[s[j]] > 1:
    #             if s[i] in dicts:
    #                 dicts[s[i]] -= 1
    #                 if dicts[s[i]] == 0:
    #                     del dicts[s[i]]
    #                 i += 1
    #     result = max(result, j - i + 1)
    #     j += 1
    # return result
    # left = max_length = 0
    # char_set = set()
    # for right in range(len(s)):
    #     while s[right] in char_set:
    #         char_set.remove(s[left])
    #         left += 1
    #     char_set.add(s[right])
    #     max_length = max(max_length, right - left + 1)
    # return max_length
    # left=max_length=0
    # count={}
    # for right,value in enumerate(s):
    #     count[value]=count.get(value,0)+1
    #     while count[value]>1:
    #         count[s[left]]-=1
    #         left+=1
    #     max_length=max(max_length,right-left+1)
    # return max_length
    left = max_length = 0
    last_seen = {}
    for right, c in enumerate(s):
        if c in last_seen and last_seen(c) >= left:
            left = last_seen[c] + 1
        max_length = max(max_length, right - left + 1)
    return max_length


def subarraySum(nums, k):
    cummulativeSum = 0
    cummulativeDicts = {}
    cummulativeDicts[0] = 1
    result = 0
    for i in range(len(nums)):
        print(cummulativeSum, cummulativeDicts, "hlo")
        cummulativeSum += nums[i]
        val = cummulativeSum - k
        if val in cummulativeDicts:
            result += cummulativeDicts[val]
        if cummulativeSum in cummulativeDicts:
            cummulativeDicts[cummulativeSum] += 1
        else:
            cummulativeDicts[cummulativeSum] = 1
    return result


def countDistinct(arr):
    # result = 0
    # for i in range(len(arr)):
    #     j = 0
    #     for j in range(i):
    #         if arr[i] == arr[j]:
    #             break
    #     if i == j + 1:
    #         result += 1

    # return result
    # arr.sort()
    # result = 1
    # for i in range(1, len(arr)):
    #     if arr[i] != arr[i - 1]:
    #         result += 1
    # return result
    print(len(set(arr)))
    result = set()
    for num in arr:
        if num not in result:
            result.add(num)
    return len(result)


# def findAnagrams(s, p):
#     dicts = {}
#     for i in range(0, len(s)):
#         abc = "".join(sorted(s[i : len(p)]))
#         print(abc, "abc")
#         if abc == "".join(sorted(p)):
#             if abc not in dicts:
#                 dicts[abc] = [i]
#             else:
#                 dicts[abc].append(i)
#     return dicts


def longestSubarray(arr):
    result = 0
    # for i in range(len(arr)):
    #     sums = arr[i]
    #     for j in range(i + 1, len(arr)):
    #         sums += arr[j]
    #         if sums == 0:
    #             result = max(result, j - i + 1)
    # return result
    dicts = {}
    prefixSum = 0
    dicts[prefixSum] = -1
    result = 0
    for i in range(len(arr)):
        prefixSum += arr[i]
        if prefixSum in dicts:
            prevIndex = dicts[prefixSum]
            length = i - prevIndex
            result = max(result, length)
        else:
            dicts[prefixSum] = i
    return result


from collections import Counter


def findAnagrams(s, p):
    # result = []
    # for i in range(len(s) - len(p) + 1):
    #     if sorted(s[i : i + len(p)]) == sorted(p):
    #         result.append(i)
    # return result
    # need = Counter(p)
    # window = {}
    # k = len(p)
    # ans = []
    # for j in range(len(s)):
    #     window[s[j]] = window.get(s[j], 0) + 1
    #     if j >= k:
    #         left = s[j - k]
    #         window[left] -= 1
    #         if window[left] == 0:
    #             del window[left]
    #     if window == need:
    #         ans.append(j - k + 1)
    # return ans
    if len(p) > len(s):
        return []
    need = [0] * 26
    window = [0] * 26
    for ch in p:
        need[ord(ch) - 97] += 1
    ans = []
    k = len(p)
    for j in range(len(s)):
        window[ord(ch) - 97] += 1
        if j >= k:
            window[ord(s[j - k]) - 97] -= 1
        if window == need:
            ans.append(j - k + 1)
    return ans


def countZeroSum(arr):
    # result = 0
    # for i in range(len(arr)):
    #     sums = arr[i]
    #     if arr[i] == 0:
    #         result += 1
    #     for j in range(i + 1, len(arr)):
    #         sums += arr[j]
    #         if sums == 0:
    #             result += 1

    # return result
    # dicts = {0: 1}
    # result = 0
    # sums = 0
    # for i in range(1, len(arr)):
    #     sums += arr[i]
    #     if sums in dicts:
    #         result += dicts[sums]
    #     dicts[sums] = dicts.get(sums, 0) + 1
    # return result
    n = len(arr)
    subarrays = [arr[i : j + 1] for i in range(n) for j in range(i, n)]
    count = sum(1 for sub in subarrays if sum(sub) == 0)
    return count


def leadersInArray(arr):
    # suffix = []
    # suffix.append(arr[-1])
    # for i in range(len(arr) - 2, -1, -1):
    #     if suffix[-1] <= arr[i]:
    #         suffix.append(arr[i])
    # return suffix[::-1]
    result = []
    n = len(arr)
    for i in range(n):
        for j in range(i + 1, n):
            if arr[i] < arr[j]:
                break
        else:
            result.append(arr[i])
    return result


def trap(height):
    n = len(height)
    total_water = 0
    # for i in range(n):
    #     left_max = 0
    #     for j in range(i + 1):
    #         left_max = max(left_max, height[j])
    #     right_max = 0
    #     for j in range(i, n):
    #         right_max = max(right_max, height[j])
    #     water = min(left_max, right_max) - height[i]
    #     if water > 0:
    #         total_water += water
    # return total_water
    # if n == 0:
    #     return 0
    # left_max = [0] * n
    # left_max[0] = height[0]
    # for i in range(1, n):
    #     left_max[i] = max(left_max[i - 1], height[i])
    # right_max = [0] * n
    # right_max[n - 1] = height[n - 1]
    # for i in range(n - 2, -1, -1):
    #     right_max[i] = max(right_max[i + 1], height[i])

    # for i in range(n):
    #     water = min(right_max[i], left_max[i]) - height[i]
    #     if water > 0:
    #         total_water += water
    # return total_water
    if n == 0:
        return 0
    if not height or len(height) < 3:
        return 0
    left = 0
    right = len(height) - 1
    left_max = height[left]
    right_max = height[right]
    total_water = 0
    while left < right:
        if left_max < right_max:
            left += 1
            left_max = max(left_max, height[left])
            water = left_max - height[left]
            if water > 0:
                total_water += water
        else:
            right -= 1
            right_max = max(right_max, height[right])
            water = right_max - height[right]
            if water > 0:
                total_water += water
    return total_water


def majorityElement(nums):
    # dicts = {}
    # for num in nums:
    #     dicts[num] = dicts.get(num, 0) + 1
    # for key, value in dicts.items():
    #     if value > len(nums) // 2:
    #         return key
    # return -1
    count = 0
    candidate = 0
    for num in nums:
        print(f"{num} num {count} count {candidate} candidate is good")
        if count == 0:
            count += 1
            candidate = num
        elif candidate == num:
            count += 1
        else:
            count -= 1
    return candidate


def search(nums, target):
    start = 0
    end = len(nums) - 1
    while start <= end:
        mid = start + (end - start) // 2
        print(f"{start} {end} {mid} ")
        if nums[mid] == target:
            return mid
        if nums[mid] >= nums[start]:
            if nums[start] <= target < nums[mid]:
                end = mid - 1
            else:
                start = mid + 1
        else:
            if nums[mid] < target <= nums[end]:
                start = mid + 1
            else:
                end = mid - 1
    return -1


def findMedianSortedArrays(nums1, nums2):
    # nums = nums1 + nums2
    # nums.sort()
    # n = len(nums)
    # if n % 2 == 0:
    #     return (nums[n // 2 - 1] + nums[n // 2]) / 2.0
    # return nums[n // 2]
    # m = len(nums1)
    # n = len(nums2)
    # i = 0
    # j = 0
    # m1 = -1
    # m2 = -1
    # for count in range((m + n) // 2 + 1):
    #     m2 = m1
    #     if i != m and j != n:
    #         if nums1[i] > nums2[j]:
    #             m1 = nums2[j]
    #             j += 1
    #         else:
    #             m1 = nums1[i]
    #             i += 1
    #     elif i < m:
    #         m1 = nums1[i]
    #         i += 1
    #     else:
    #         m1 = nums2[j]
    #         j += 1
    # return m1 if (m + n) % 2 == 1 else (m1 + m2) / 2.0
    if len(nums1) > len(nums2):
        nums1, nums2 = nums2, nums1
    m = len(nums1)
    n = len(nums2)
    left, right = 0, m
    while left <= right:
        i = (left + right) // 2
        j = (m + n + 1) // 2 - i
        left1 = nums1[i - 1] if i > 0 else float("-inf")
        right1 = nums1[i] if i < m else float("inf")
        left2 = nums2[j - 1] if j > 0 else float("-inf")
        right2 = nums2[j] if j < n else float("inf")
        if left1 <= right2 and right1 <= left2:
            if (m + n) % 2 == 0:
                return (max(left1, left2) + min(right1, right2)) / 2.0
            else:
                # Odd: max of left side
                return max(left1, left2)
        elif left1 > right2:
            # i too large, move left
            right = i - 1
        else:
            # i too small, move right
            left = i + 1
    return 0.0


def allFunctions(arr):
    n = len(arr)
    ngE = [-1] * len(arr)
    stack = []
    for i in range(n):
        while stack and arr[stack[-1]] < arr[i]:
            idx = stack.pop()
            ngE[idx] = arr[i]
        stack.append(i)
    ngL = [-1] * len(arr)
    stack = []
    for i in range(n - 1, -1, -1):
        while stack and arr[stack[-1]] < arr[i]:
            idx = stack.pop()
            ngL[idx] = arr[i]
        stack.append(i)
    nsL = [-1] * len(arr)
    stack = []
    for i in range(n - 1, -1, -1):
        while stack and arr[stack[-1]] > arr[i]:
            idx = stack.pop()
            nsL[idx] = arr[i]
        stack.append(i)
    nsR = [-1] * len(arr)
    stack = []
    for i in range(n):
        while stack and arr[stack[-1]] > arr[i]:
            idx = stack.pop()
            nsR[idx] = arr[i]
        stack.append(i)


import heapq
from collections import deque


def sildingWindowMaximum(arr, k):
    heap = []
    result = []
    for i in range(len(arr) - k + 1):
        result.append(max(arr[i : i + k]))
    print(result, "o(n)*o(k)")
    result = []
    for i in range(k):
        heapq.heappush(heap, (-arr[i], i))
    result.append(-1 * heap[0][0])
    for i in range(k, len(arr)):
        heapq.heappush(heap, (-arr[i], i))
        print(heap)
        while heap[0][1] <= i - k:
            heapq.heappop(heap)
        result.append(-1 * heap[0][0])
    print(result)
    n = len(arr)
    result = []
    dq = deque()
    for i in range(0, k):
        while dq and arr[i] >= arr[dq[-1]]:
            dq.pop()
        dq.append(i)
    for i in range(k, len(arr)):
        result.append(arr[dq[0]])
        while dq and dq[0] <= i - k:
            dq.popleft()
        while dq and arr[i] >= arr[dq[-1]]:
            dq.pop()
        dq.append(i)
    result.append(arr[dq[0]])
    print(result)


# print(sildingWindowMaximum([1, 3, 2, 1, 7, 3], k=3))


def rotate(arr):
    for i in range(len(arr)):
        for j in range(i + 1, len(arr[0])):
            arr[i][j], arr[j][i] = arr[j][i], arr[i][j]
        arr[i] = arr[i][::-1]
    return arr


class StockSpanner:

    def __init__(self):
        # self.price = []
        self.stack = []

    def next(self, price: int) -> int:
        # self.price.append(price)
        # span = 1
        # print(self.stack, self.price)
        # while self.stack and self.price[self.stack[-1]] <= price:
        #     self.stack.pop()
        # if self.stack:
        #     span = len(self.price) - 1 - self.stack[-1]
        # else:
        #     span = len(self.price)
        # self.stack.append(len(self.price) - 1)
        # return span
        span = 1
        while self.stack and self.stack[-1][0] <= price:
            span += self.stack[-1][1]
            self.stack.pop()
        self.stack.append((price, span))
        return span


def largestRectangleArea(arr):
    n = len(arr)
    nsL = [-1] * len(arr)
    stack = []
    for i in range(n):
        while stack and arr[stack[-1]] >= arr[i]:
            stack.pop()
        nsL[i] = stack[-1] if stack else -1
        stack.append(i)
    nsR = [n] * len(arr)
    stack = []
    for i in range(n - 1, -1, -1):
        while stack and arr[stack[-1]] >= arr[i]:
            stack.pop()
        nsR[i] = stack[-1] if stack else n
        stack.append(i)
    maxs = 0
    for i in range(n):
        area = arr[i] * (nsR[i] - nsL[i] - 1)
        maxs = max(maxs, area)
    return maxs


from collections import deque


def reverseQueue(queue: deque) -> deque:
    stack = []
    while queue:
        stack.push(queue.popleft())
    while stack:
        queue.append(stack.pop())
    return queue


class MinStack:
    def __init__(self):
        self.stack = []
        self.min_stack = []

    def push(self, val: int) -> None:
        self.stack.append(val)
        if not self.min_stack and self.min_stack[-1] >= val:
            self.min_stack.append(val)

    def pop(self) -> None:
        val = self.stack.pop()
        if val == self.min_stack[-1]:
            self.min_stack.pop()

    def top(self) -> int:
        return self.stack[-1]

    def getMin(self) -> int:
        return self.min_stack[-1]


class MinStackSingleStack:
    def __init__(self):
        self.stack = []
        self.curr_min = float("inf")

    def push(self, val: int) -> None:
        if self.curr_min >= val:
            self.stack.append(self.curr_min)
            self.curr_min = val
        self.stack.append(val)

    def top(self) -> int:
        return self.stack[-1]

    def getMin(self) -> int:
        return self.curr_min

    def pop(self):
        if not self.stack:
            return
        val = self.stack.pop()
        if val == self.curr_min:
            self.curr_min = self.stack.pop()


class Node:
    def __init__(self, val):
        self.value = val
        self.next = None


class Queue:
    def __init__(self):
        self.front = None
        self.rear = None
        self.size = 0

    def enqueue(self, value):
        new_node = Node(value)
        if self.is_empty():
            self.front = new_node
            self.rear = new_node
        else:
            self.rear.next = new_node
            self.rear = new_node
        self.size += 1

    def dequeue(self):
        if self.is_empty():
            return None
        value = self.front.value
        self.front = self.front.next
        if self.front is None:
            self.rear = None
        self.size -= 1
        return value

    def peek(self):
        if self.is_empty():
            return None
        return self.front.value

    def is_empty(self):
        return self.front is None

    def get_size(self):
        return self.size


class DequeImplementation:
    @staticmethod
    def show_operations():
        dq = deque()
        dq.append(1)
        dq.appendleft(2)
        dq.append(3)
        print(dq)

        right = dq.pop()
        left = dq.popleft()

        print(dq)

        print(dq[0])
        print(dq[-1])

        dq = deque([1, 2, 3, 4, 5])
        dq.rotate(2)
        dq.rotate(-1)


def compare_performance():
    import time
    from collections import deque

    # List as queue - SLOW!
    start = time.time()
    lst = []
    for i in range(10000):
        lst.append(i)
    for i in range(10000):
        lst.pop(0)  # O(n) each time!
    print(f"List: {time.time() - start:.4f} seconds")

    # Deque as queue - FAST!
    start = time.time()
    dq = deque()
    for i in range(10000):
        dq.append(i)
    for i in range(10000):
        dq.popleft()  # O(1) each time!
    print(f"Deque: {time.time() - start:.4f} seconds")


def nextGreaterElementRight(arr):
    n = len(arr)
    ngE = [n] * len(arr)
    stack = []
    for i in range(n):
        while stack and arr[stack[-1]] < arr[i]:
            idx = stack.pop()
            ngE[idx] = i
        stack.append(i)
    print(ngE)


def removeKDigits(num, k):
    stack = []

    for digit in num:
        while k > 0 and stack and stack[-1] > digit:
            stack.pop()
            k -= 1
        stack.append(digit)
    if k > 0:
        stack = stack[:-k]
    result = "".join(stack).lstrip("0")
    return result if result else "0"


def asteroidCollision(arr):
    stack = []
    for asteroid in arr:
        survives = True
        while stack and stack[-1] > 0 and asteroid < 0:
            if stack[-1] + asteroid == 0:
                stack.pop()
                survives = False
                break
            elif stack[-1] < -asteroid:
                stack.pop()
            else:
                survives = False
                break
        if survives:
            stack.append(asteroid)
    return stack


from typing import Optional


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def create_linked_list(arr):
    if not arr:
        return None

    head = ListNode(arr[0])
    current = head
    for val in arr[1:]:
        current.next = ListNode(val)
        current = current.next
    return head


class Solution:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        head = create_linked_list(head)
        arr = []
        while head is not None:
            arr.append(head.val)
            head = head.next
        arr = arr[::-1]
        newHead = ListNode(arr[1])
        for val in arr[1:]:
            newHead.next = ListNode(val)
            newHead = newHead.next
        print(arr)
        prev = None
        current = head
        while current:
            next_temp = current.next
            current.next = prev
            prev = current
            current = next_temp
        return prev

    def find_middle(self, head: Optional[ListNode]) -> Optional[ListNode]:
        slow = fast = head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
        return slow

    def hasCycle(self, head: Optional[ListNode]) -> bool:
        slow = fast = head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.nxt
            if slow == fast:
                return True
        return False

    def detectCycle(self, head: Optional[ListNode]) -> Optional[ListNode]:
        slow = fast = head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.nxt
            if slow == fast:
                slow = head
                while slow != fast:
                    slow = slow.next
                    fast = fast.next
                return slow
        return None

    def getNthNode(self, head: Optional[ListNode], N: int) -> Optional[ListNode]:
        current = head
        for i in range(N):
            if not current:
                return None
            current = current.next
        return current

    def findNthFromEnd(self, head: Optional[ListNode], N: int) -> Optional[ListNode]:
        fast = slow = head
        for i in range(N):
            if not fast:
                return None
            fast = fast.next
        if not fast:
            return head.next
        while fast:
            slow = slow.next
            fast = fast.next
        slow.next = slow.next.next
        return head

    def addTwoNumbers(
        self, head1: Optional[ListNode], head2: Optional[ListNode]
    ) -> Optional[ListNode]:
        addHead = ListNode(None)
        current = addHead
        rem = 0
        while not head1 and not head2 and rem:
            sum1 = head1.val + head2.val + rem
            rem = sum1 // 10
            digit = sum1 % 10
            current.next = ListNode(digit)
            current = current.next
            head1 = head1.next if head1 else None
            head2 = head2.next if head1 else None
        return addHead.next

    def mergeTwoLists(
        self, list1: Optional[ListNode], list2: Optional[ListNode]
    ) -> Optional[ListNode]:
        mergeList = ListNode(None)
        current = mergeList
        while list1 and list2:
            if list1.val > list2.val:
                current.next = list2
                list2 = list2.next if list2 else None
            elif list1.val <= list2.val:
                current.next = list1
                list1 = list1.next if list1 else None
            current = current.next
        if list1:
            current.next = list1
        if list2:
            current.next = list2
        return mergeList.next


class AllStackFunc:
    def __init__(self, arr):
        self.arr = arr
        self.n = len(self.arr)
        self.ngl = [-1] * self.n
        self.ngr = [-1] * self.n
        self.nsl = [-1] * self.n
        self.nsR = [self.n] * self.n

    def greaterToRight(self):
        stack = []
        for i in range(self.n):
            while stack and self.arr[stack[-1]] >= self.arr[i]:
                idx = stack.pop()
                self.ngr[idx] = i
            stack.append(i)

    def greaterToLeft(self):
        stack = []
        for i in range(self.n - 1, -1, -1):
            while stack and self.arr[stack[-1]] >= self.arr[i]:
                idx = stack.pop()
                self.ngl[idx] = i
            stack.append(i)

    def smallerToLeft(self):
        stack = []
        for i in range(self.n - 1, -1, -1):
            while stack and self.arr[stack[-1]] <= self.arr[i]:
                idx = stack.pop()
                self.nsl[idx] = i
            stack.append(i)

    def smallerToRight(self):
        stack = []
        for i in range(self.n):
            while stack and self.arr[stack[-1]] <= self.arr[i]:
                idx = stack.pop()
                self.nsR[idx] = i
            stack.append(i)


def max_in_k(arr, k):
    deque = []
    result = []
    for i in range(len(arr)):
        while deque and deque[0] <= i - k:
            deque.pop()
        while deque and arr[deque[-1]] <= arr[i]:
            deque.pop()
        deque.append(i)

        if i >= k - 1:
            result.append(arr[deque[0]])
    return deque


def productSelf(arr):
    # product = [1] * len(arr)
    # for i in range(len(arr)):
    #     for j in range(len(arr)):
    #         if i != j:
    #             product[i] = product[i] * arr[j]

    # return product
    # rightProduct = [1] * len(arr)
    # leftProduct = [1] * len(arr)
    # for i in range(1, len(arr)):
    #     rightProduct[i] = arr[i - 1] * rightProduct[i - 1]
    # for i in range(len(arr) - 2, -1, -1):
    #     leftProduct[i] = arr[i + 1] * leftProduct[i + 1]
    # result = [1] * len(arr)
    # for i in range(len(arr)):
    #     result[i] = rightProduct[i] * leftProduct[i]
    # return result
    zeros = 0
    idx = -1
    prod = 1
    for i in range(len(arr)):
        if arr[i] == 0:
            zeros += 1
            idx = i
        else:
            prod *= arr[i]
    res = [0] * len(arr)
    if zeros == 0:
        for i in range(len(arr)):
            res[i] = prod // arr[i]
    elif zeros == 1:
        res[idx] = prod

    return res


import heapq


def findKthLargest(nums, k):
    heap = []
    for num in nums:
        heapq.heappush(heap, -num)
    value = -1
    while k > 0:
        value = heapq.heappop(heap)
        k -= 1
    return -value


def findKthSmallest(nums, k):
    heap = []
    # for num in nums:
    #     heapq.heappush(heap, num)
    # value = -1
    # while k > 0:
    #     value = heapq.heappop(heap)
    #     k -= 1
    # return value
    for i in range(len(nums)):
        for j in range(len(nums[0])):
            heapq.heappush(heap, -nums[i][j])
            if len(heap) > k:
                break
    return -heap[0]


def kthSmallestMatrix(mat, k):
    heap = []
    for i in range(min(k, len(mat[0]))):
        heap.heappush(heap, (mat[i][0], i, 0))
    for _ in range(k):
        val, i, j = heapq.heappop(heap)
        if j + 1 < len(mat[0]):
            heapq.heappush(heap, (mat[i][j + 1], i, j + 1))
    return val


def connectNRopes(arr):
    result = 0
    heap = []
    for value in arr:
        heapq.heappush(heap, value)
    while heap and len(heap) > 1:
        a, b = heapq.heappop(heap), heapq.heappop(heap)
        result += a + b
        heapq.heappush(heap, a + b)
    return result


def smashLargestStone(arr):
    heap = []
    result = 0
    for num in arr:
        heapq.heappush(heap, -num)
    while heap and len(heap) > 1:
        a, b = heapq.heappop(heap), heapq.heappop(heap)
        value = -1 * a - -1 * b
        result += value
        if value != 0:
            heapq.heappush(heap, -(value))
    return -1 * heap[0]


def minimumOperations(nums):
    # heap = []
    # count = 0
    # for num in nums:
    #     if num > 0:
    #         heapq.heappush(heap, num)
    # while heap:
    #     smallest = heapq.heappop()
    #     if smallest == 0:
    #         continue
    #     count += 1
    #     newHeap = []
    #     while heap:
    #         val = heapq.heappop()
    #         if val - smallest > 0:
    #             heapq.heappush(newHeap, val - smallest)
    #     heap = newHeap
    # return count
    unique_positive = {num for num in nums if num > 0}
    return len(unique_positive)


def topKFrequent(nums, k):
    dicts = {}
    for num in nums:
        dicts[num] = dicts.get(num, 0) + 1
    heap = []
    for key, values in dicts.items():
        heapq.heappush(heap, (-values, key))
    result = []
    while k > 0 and heap:
        value, key = heapq.heappop(heap)
        result.append(key)
        k -= 1
    return result


import math


def kClosest(points, k):
    heap = []
    result = []
    for point in points:
        x1, y1 = point
        values = math.sqrt(x1 * x1 + y1 * y1)
        heapq.heappush(heap, (values, [x1, y1]))
        if len(heap) > k:
            heap.heappop(heap)
    return [point for dist, point in heap]
    # while k > 0 and heap:
    #     value, point = heapq.heappop(heap)
    #     result.append(point)
    #     k -= 1
    # return result


def activitySelection(finish, start):
    heap = []
    ans = 0
    for i in range(len(finish)):
        heapq.heappush(heap, (finish[i], start[i]))
    finishtime = -1
    while heap:
        activity = heapq.heappop(heap)
        if activity[1] >= finishtime:
            finishtime = activity[0]
            ans += 1
    return ans


def fractionalKnapsack(val, wt, capacity):
    n = len(val)
    items = [[val[i], wt[i]] for i in range(n)]
    heap = []
    for value in items:
        val, wt = value
        heapq.heappush(heap, (val / wt, wt, val))
    res = 0.0
    currentCapacity = capacity
    while capacity > 0 and heap:
        ratio, wt, val = heapq.heappop(heap)
        if currentCapacity >= wt:
            res += val
            currentCapacity -= wt
        else:
            res += ratio * currentCapacity
            break
    return res


def numRescueBoats(people, limit):
    # n = len(people)
    # heap = []
    # result = []
    # for p in people:
    #     heapq.heappush(heap, p)
    # while heap:
    #     heaviest = heapq.heappop(heap)
    #     if heaviest and heap[0] + heaviest <= limit:
    #         heapq.heappop()
    #     boats += 1
    # return boats
    people.sort()
    start, end = 0, len(people) - 1
    boats = 0
    while start <= end:
        if people[end] + people[start] <= limit:
            start += 1
        end -= 1
        boats += 1
    return boats


def minPlatform(arr, dep):
    n = len(arr)
    res = 0
    arr.sort()
    dep.sort()
    cnt = 1
    i = 0
    j = 0
    while i < n and j < n:
        if arr[i] <= dep[j]:
            i += 1
            cnt += 1
        else:
            cnt -= 1
            j += 1
        result = max(cnt, result)
    return result


def maxOccupancy(entries, exit):
    events = []

    for i in range(len(entries)):
        events.append((entries[i], +1))
        events.append((exit[i], -1))
    events.sort()
    current = 0
    max_people = 0
    for time, change in events:
        current += change
        max_people = max(max_people, current)
    return max_people


def minMeetingRooms(intervals):
    events = []
    for start, end in intervals:
        events.append((start, +1))
        events.append((end, -1))
    events.sort()
    max_poeple = 0
    current = 0
    for time, change in events:
        current += change
        max_people = max(max_people, current)
    return max_people


def carPooling(trips, capacity):
    events = []
    for p, start, end in trips:
        events.append((start, p))
        events.append((end, -p))
    current = 0
    for time, p in events:
        current += p
        if current > capacity:
            return False
    return True


def getSkyline(buildings):
    events = []
    for l, r, h in buildings:
        events.append((l, -h))
        events.append((r, h))
    events.sort()
    heap = [0]
    prev_heights = 0
    result = []
    for x, h in events:
        if h < 0:
            heapq.heappush(heap, h)
        else:
            heap.remove(-h)
            heapq.heapify(heap)
        current_height = -heap[0]  # Max height

        if current_height != prev_height:
            result.append([x, current_height])
            prev_height = current_height
    return result


def jobSequencing(deadline, profit):
    n = len(deadline)
    # cnt = 0
    # totalProfit = 0
    # jobs = [(profit[i], deadline[i]) for i in range(n)]
    # jobs.sort(key=lambda x: x[0], reverse=True)
    # slot = [0] * n
    # for i in range(n):
    #     start = min(n, jobs[i][1]) - 1
    #     for j in range(start, -1, -1):
    #         if slot[0] == 0:
    #             slot[j] = 1
    #             cnt += 1
    #             totalProfit += jobs[j][0]
    #             break
    # return [cnt, totalProfit]
    ans = [0, 0]
    jobs = [(deadline[i], profit[i]) for i in range(n)]
    jobs.sort()
    pq = []
    for job in jobs:
        # if job[0] > len(pq):
        #     heapq.heappush(pq, job[1])
        # elif pq and pq[0] < job[1]:
        #     heapq.heappop(pq)
        #     heapq.heappush(pq, job[1])
        if job[0] > len(pq):
            heapq.heappush(pq, job[1])
        elif pq and pq[0] < job[1]:
            heapq.heappop(pq)
            heapq.heappush(pq, job[1])
    while pq:
        ans[1] += heapq.heappop(pq)
        ans[0] += 1
    return ans


def numberOfSpecialChars(word):
    # dicts = {}
    # count = 0
    # for w in word:
    #     if w == w.upper() and w.lower() in dicts:
    #         count += 1
    #     dicts[w] = dicts.get(w, 0) + 1
    # return count
    dictsSmall = {}
    dictsBig = {}
    for i in range(len(word)):
        w = word[i]
        if w == w.upper():
            dictsBig[w] = i
        else:
            dictsSmall[w] = i
    count = 0
    for key in dictsSmall.keys():
        if key.upper() in dictsBig and dictsBig[key.upper()] > dictsSmall[key]:
            count += 1
    return count


class DoublyLinkedList:
    def __init__(self, key, val, prev, next):
        self.key = key
        self.val = val
        self.prev = prev
        self.next = next


class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.size = 0
        self.cache = {}
        self.head = Node(0, 0)
        self.tail = Node(0, 0)
        self.head.next = self.tail
        self.tail.prev = self.head

    def get(self, key: int):
        if key not in self.cache:
            return -1
        node = self.cache[key]
        self._move_to_front(node)
        return node.val

    def _add_to_front(self, node):
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node

    def _remove_node(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev

    def _move_to_front(self, node):
        self._remove_node(node)
        self._add_to_front(node)

    def put(self, key, value):
        if key in self.cache:
            node = self.cache[key]
            node.val = value
            self._move_to_front(node)

        node = Node(key, value)
        self.cache[key] = node
        self._add_to_front(node)
        self.size += 1
        if self.size > self.capacity:
            lru = self.tail.prev
            self._remove_node(lru)
            del self.cache[lru.key]
            self.size -= 1


class LFUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.size = 0
        self.cache = {}
        self.head = Node(0, 0)
        self.tail = Node(0, 0)
        self.head.next = self.tail
        self.tail.prev = self.head
        self.freqToList = {}
        self.heap = []

    def get(self, key: int):
        if key not in self.cache:
            return -1
        node = self.cache[key]
        self._move_to_front(node)
        self.freqToList[key] = self.freqToList.get(key, 0) + 1
        heapq.heappush(self.heap, (key, self.freqToList[key]))
        return node.val

    def _add_to_front(self, node):
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node

    def _remove_node(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev

    def _move_to_front(self, node):
        self._remove_node(node)
        self._add_to_front(node)

    def put(self, key, value):
        if key in self.cache:
            node = self.cache[key]
            node.val = value
            self.freqToList[key] += 1
            heapq.heappush(self.heap, (key, self.freqToList[key]))
