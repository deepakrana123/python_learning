class SegmentTree:
    def __init__(self, data, function, default):
        self.n = len(data)
        self.func = function
        self.default = default
        self.size = 1
        while self.size < self.n:
            self.size *= 2
        self.tree = [default] * (2 * self.size)
        self._build(data)

    def _build(self, data):
        for i in range(len(data)):
            self.tree[self.size + i] = data[
                i
            ]  # sending leaves node or building leaves node
        for i in range(self.size - 1, 0, -1):
            self.tree[i] = self.func(self.tree[2 * i + 1], self.tree[2 * i + 2])

    def update(self, index, value):
        pos = self.size + index
        self.tree[pos] = value
        while pos > 1:
            pos //= 2
            self.tree[pos] = self.func(self.tree[2 * pos], self.tree[2 * pos + 1])

    def query(self, l, r):
        l += self.size
        r += self.size
        res = self.default

        while l < r:
            if l % 2:
                res = self.func(res, self.tree[l])
                l += 1
            if r % 2:
                r -= 1
                res = self.func(res, self.tree[r])
            l //= 2
            r //= 2
        return res


class SegmentTreeRecusrive:
    def __init__(self, data):
        self.n = len(data)
        self.segTree = [0] * (self.n)
        self.buildSegmentTree(0, 0, self.n - 1, data)

    def buildSegmentTree(self, index, start, end, data):
        if start == end:
            self.segTree[index] = data[start]
        mid = start + (end - start) // 2
        self.buildSegmentTree(2 * index + 1, start, mid, data)
        self.buildSegmentTree(2 * index + 2, mid + 1, end, data)
        self.segTree[index] = self.segTree[2 * index + 1] + self.segTree[2 * index + 2]

    def updateSegmentTree(self, index, val, i, start, end, data):
        if start == end:
            self.segTree[i] = val
            return
        mid = start + (end - start) // 2
        if index <= mid:
            self.updateSegmentTree(index, val, 2 * i + 1, start, mid, data)
        else:
            self.updateSegmentTree(index, val, 2 * i + 2, mid + 1, end, data)
        self.segTree[i] = self.segTree[2 * i + 1] + self.segTree[2 * i + 2]

    def update(self, index, val):
        self.updateSegmentTree(index, val, 0, 0, self.n - 1)

    def querySegmentTree(self, left, right, index, start, end, data):
        if start > right or end > left:
            return 0
        elif start >= left and end <= right:
            return self.segTree[index]
        mid = start + (end - start) // 2
        return self.querySegmentTree(
            left, right, 2 * index + 1, start, mid + 1, data
        ) + self.querySegmentTree(left, right, 2 * index + 2, mid, end, data)


class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children
        node.is_end = True

    def search(self, word):
        node = self.root
        for ch in word:
            if ch not in node.children:
                return False
            node = node.children[ch]
        return node.is_end

    def startWith(self, prefix):
        node = self.root
        for ch in prefix:
            if ch not in node.children:
                return False
            node = node.children[ch]
        return True


def maximumUniqueSubarray(nums):
    i = 0
    j = len(nums)
    ans = -1
    sums = 0

    def getBoolean(dicts, curr):
        if curr in dicts and dicts[curr] == 2:
            return True
        return False

    dicts = {}
    while i <= j:
        if nums[j] in dicts:
            while nums[j] in dicts and getBoolean(dicts, nums[j]):
                sums -= nums[i]
                dicts[nums[i]] -= 1
                if dicts[nums[i]] == 0:
                    del dicts[nums[i]]
            sums += nums[j]
            dicts[nums[j]] = dicts.get(nums[j], 0) + 1
            j += 1
            ans = max(sums, ans)
    return ans
