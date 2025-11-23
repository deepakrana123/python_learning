class SegmentTree:
    def __init__(self, data, function, default):
        self.n = len(data)
        self.func = function  # e.g., sum, min, max
        self.default = default
        self.size = 1
        while self.size < self.n:
            self.size *= 2
        self.tree = [default] * (2 * self.size)
        self._build(data)

    def _build(self, data):
        # Fill the leaves
        for i in range(len(data)):
            self.tree[self.size + i] = data[i]
        # Build the tree by merging children
        for i in range(self.size - 1, 0, -1):
            self.tree[i] = self.func(self.tree[2 * i], self.tree[2 * i + 1])

    def update(self, index, value):
        # Set value at position index
        pos = self.size + index
        self.tree[pos] = value
        while pos > 1:
            pos //= 2
            self.tree[pos] = self.func(self.tree[2 * pos], self.tree[2 * pos + 1])

    def query(self, l, r):
        # Query in interval [l, r)
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


# def update(i, l, r, index, value, s):
#     if l == r:
#         s[i] = value
#         return
#     mid = (l + r) // 2
#     if index <= mid:
#         update(2 * i + 1, l, mid, index, value)
#     else:
#         update(2 * i + 2, mid + 1, r, index, value)
#     s[i] = function(s[2 * i + 1], s[2 * i + 2])  # merge step


class NumArray:
    def __init__(self, nums):
        self.n = len(nums)
        self.segTree = [0] * (4 * self.n)
        self.buildSegmentTree(0, 0, self.n - 1, nums)

    def buildSegmentTree(self, index, start, end, nums):
        if start == end:
            self.segTree[index] = nums[start]
            return
        mid = start + (end - start) // 2
        self.buildSegmentTree(2 * index + 1, start, mid, nums)
        self.buildSegmentTree(2 * index + 2, mid + 1, end, nums)
        self.segTree[index] = self.segTree[2 * index + 1] + self.segTree[2 * index + 2]

    def updateSegmentTree(self, index, val, i, start, end):
        if start == end:
            self.segTree[i] = val
            return
        mid = start + (end - start) // 2
        if index <= mid:
            self.updateSegmentTree(index, val, 2 * i + 1, start, mid)
        else:
            self.updateSegmentTree(index, val, 2 * i + 2, mid + 1, end)
        self.segTree[i] = self.segTree[2 * i + 1] + self.segTree[2 * i + 2]

    def update(self, index, val):
        self.updateSegmentTree(index, val, 0, 0, self.n - 1)

    def querySegmentTree(self, left, right, index, start, end):
        if start > right or end < left:
            return 0
        elif start >= left and end <= right:
            return self.segTree[index]
        mid = start + (end - start) // 2
        return self.querySegmentTree(
            left, right, 2 * index + 1, start, mid + 1
        ) + self.querySegmentTree(left, right, 2 * index + 2, mid, end)

    def sumRange(self, left, right):
        return self.querySegmentTree(left, right, 0, 0, self.n - 1)

    # result = []

    # def RMIQ(segmentTree, heights, size, start, end):
    #     return querySegmentTree(
    #         start, end, segmentTree, heights, 0, size - 1, left, mid
    #     )

    # def querySegmentTree(start, end, segmentTree, heights, index, n, left, mid):
    #     if left > start and r < end:
    #         return -1

    #     if left >= start and r <= end:
    #         return segmentTree[index]
    #     mid = left + (right - left) // 2
    #     leftIndex = querySegmentTree(
    #         start, end, 2 * index + 1, left, mid, segmentTree, heights
    #     )
    #     rightIndex = querySegmentTree(
    #         start, end, 2 * index + 2, mid + 1, len(heights), segmentTree, heights
    #     )
    #     if leftIndex != -1:
    #         return rightIndex
    #     if rightIndex != -1:
    #         return leftIndex

    #     return leftIndex if heights[leftIndex] >= heights[rightIndex] else rightIndex

    # def constructSegmentTree(heights, size):
    #     segTree = []

    #     def construct(index, start, end):
    #         if start == end:
    #             segTree[index] = end
    #             return
    #         mid = start + (end - start) // 2
    #         construct(2 * index + 1, start, mid)
    #         construct(2 * index + 2, mid + 1, end)
    #         if heights(segTree[2 * index + 1]) > heights(segTree[2 * index + 2]):
    #             segTree[index] = 2 * index + 1
    #         else:
    #             segTree[index] = 2 * index + 2

    #     return segTree

    # segmentTree = constructSegmentTree(heights, len(heights))

    # for l, r in queries:
    #     if l == r:
    #         result.append(heights[l])
    #         continue
    #     maxIndex = max(l, r)
    #     minIndex = min(l, r)
    #     if heights[maxIndex] > heights[minIndex]:
    #         result.append(heights[maxIndex])
    #         continue
    #     else:
    #         left = maxIndex + 1
    #         right = len(heights)
    #         result_Max = float("inf")
    #         while left <= right:
    #             mid = left + (right - left) // 2
    #             idx = RMIQ(segmentTree, heights, len(heights), left, mid)
    #             if heights[idx] > max(heights[minIndex], heights[maxIndex]):
    #                 result_Max = min(idx, result_Max)
    #                 r = mid - 1
    #             else:
    #                 l = mid - 1
    #         if result_Max == float("inf"):
    #             result.append(-1)
    #         else:
    #             result.append(result_Max)
    # return result


def leftmostBuildingQueries(heights, queries):
    n = len(heights)
    result = []
    size = 4 * n
    seg_tree = [0] * size

    def build(index, l, r):
        if l == r:
            seg_tree[index] = l
            return
        mid = l + (r - l) // 2
        build(2 * index + 1, l, mid)
        build(2 * index + 1, mid + 1, r)
        if heights(seg_tree[2 * index + 1]) >= heights(seg_tree[2 * index + 2]):
            seg_tree[index] = seg_tree[2 * index + 1]
        else:
            seg_tree[index] = seg_tree[2 * index + 2]

    def query(index, l, r, ql, qr):
        if qr < l or ql > r:
            return -1
        if ql <= l and r <= qr:
            return seg_tree[index]

        mid = (l + r) // 2
        left_res = query(2 * index + 1, l, mid, ql, qr)
        right_res = query(2 * index + 2, mid + 1, r, ql, qr)
        if left_res != -1:
            return left_res
        if right_res != -1:
            return right_res
        return left_res if heights[left_res] >= heights[right_res] else right_res

    build(0, 0, n - 1)
    for l, r in queries:
        if l == r:
            result.append(heights[l])
            continue
        if heights[r] > heights[l]:
            result.append(r)
            return
        val = max(heights[l], heights[r])
        low = max(l, r) + 1
        high = n - 1
        ans = -1
        while low <= high:
            mid = low + (high - low) // 2
            idx = query(0, 0, n - 1, max(l, r) + 1, mid)
            if idx != -1 and heights[idx] > max(heights[l], heights[r]):
                ans = idx
                high = mid - 1
            else:
                low = mid + 1
        result.append(ans)
    return result


def leftmostBuildingQueries1(heights, queries):
    n = len(heights)
    result = [-1] * len(queries)
    next_greater = [-1] * n
    stack = []
    for i in range(n - 1, -1, -1):
        while stack and heights[stack[-1]] < heights[i]:
            stack.pop()
            if stack:
                next_greater[i] = stack[-1]
            stack.append(-1)
    for i, (l, r) in enumerate(queries):
        if l == r:
            result[i] = heights[l]
        elif heights[r] > heights[l]:
            result[i] = heights[r]
        else:
            max_height = max(heights[l], heights[r])
            idx = max(l, r)
            while idx != -1 and heights[idx] <= max_height:
                idx = next_greater[idx]
            result[i] = idx if idx != -1 else -1
    return result


class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False
        self.count = 0


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word, i):
        node = self.root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
            node.count += 1
        node.is_end = True

    def search(self, word):
        node = self.root
        for ch in word:
            if ch not in node.children:
                return False
            node = node.children[ch]
        return node.is_end

    def startsWith(self, prefix):
        node = self.root
        for ch in prefix:
            if ch not in node.children:
                return 0
            node = node.children[ch]
        return node.count


def prefixCount(self, words, pref):
    prefixTire = Trie()
    for word in words:
        prefixTire.insert(word)

    return prefixTire.startsWith(pref)


def countPrefixSuffixPairs(words):
    count = 0
    # for i in range(len(words)):
    #     for j in range(i + 1, len(words)):
    #         if (
    #             words[i] == words[j][0 : len(words[i])]
    #             and words[i] == words[j][-len(words[i]) :]
    #         ):
    #             count += 1
    # return count
    for i in range(len(words)):
        prefixTrie = Trie()
        suffixTrie = Trie()
        prefixTrie.insert(words[i])
        suffixTrie.insert(words[i][::-1])
        for j in range(0, i):
            if len(words[j]) > len(words[i]):
                continue
            if prefixTrie.search(words[j]) and suffixTrie.search(words[j][::-1]):
                count += 1
    return count


class TrieNode:
    def __init__(self):
        self.is_end_of_word = False
        self.children = {}


class WordDictionary:
    def __init__(self):
        self.root = TrieNode()

    def addWord(self, word: str) -> None:
        crawl = self.root
        for char in word:
            if char not in crawl.children:
                crawl.children[char] = TrieNode()
            crawl = crawl.children[char]
        crawl.is_end_of_word = True

    def search_utils(self, node, word):
        for i in range(len(word)):
            char = word[i]
            if char == ".":
                for child in node.children:
                    if self.search_utils(node.children[child], word[i + 1 :]):
                        return True
                return False
            else:
                if char not in node.children:
                    return False
                node = node.children[char]
        return node.is_end_of_word

    def search(self, word: str) -> bool:
        return self.search_utils(self.root, word)


class TrieNodes:
    def __init__(self):
        self.children = {}
        self.is_end = False


class Tries:
    def __init__(self):
        self.root = TrieNodes()

    def insert(self, word):
        node = self.root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNodes()
            node = node.children[ch]
        node.is_end = True

    def search(self, word):
        node = self.root
        for i in range(len(word)):
            ch = word[i]
            if ch not in node.children:
                return word
            node = node.children[ch]
            if node.is_end:
                return word[0 : i + 1]
        return word


def replaceWords(dictionary, sentence):
    words = Tries()
    for w in dictionary:
        words.insert(w)
    l = sentence.split(" ")
    sen = ""
    for word in l:
        sen += words.search(word) + " "
    return sen.strip(" ")


class WordBreakTrie:
    def __init__(self):
        self.root = TrieNodes()

    def insert(self, word):
        node = self.root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNodes()
            node = node.children[ch]
        node.is_end = True

    def search(self, word, start, memo):
        if start in memo:
            return memo[start]
        crawl = self.root
        for i in range(start, len(word)):
            if word[i] not in crawl.children:
                memo[i] = False
                return False
            crawl = crawl.children[word[i]]
            if crawl.is_end:
                if i == len(word) - 1 or self.search(word, i + 1, memo):
                    memo[start] = True
                    return True
        memo[i] = True
        return False


def wordBreak(s, wordDict):
    memo = {}
    wordBreaks = WordBreakTrie()
    for words in wordDict:
        wordBreaks.insert(words)

    # return wordBreaks.search(s, 0, memo)
    # only recusrion
    def solve(idx, s):
        if idx == len(s):
            return True
        if s in wordDict:
            return True
        for i in range(len(s) + 1):
            temp = s[idx:i]
            if temp in wordDict and solve(i + idx, s):
                return True
        return False

    return solve(0, s)


class FindWordsTrieStr:
    def __init__(self):
        self.children = {}
        self.is_end = False
        self.words = ""


class FindWordsTrie:
    def __init__(self):
        self.root = FindWordsTrieStr()

    def insert(self, word):
        node = self.root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = FindWordsTrieStr()
            node = node.children[ch]
        node.is_end = True
        node.words = word

    def search(self, word):
        node = self.root
        for ch in word:
            if ch not in node.children:
                return {False, ""}
            node = node.children[ch]
        return {node.is_end, node.words}


def findWords(board, words):
    n = len(board[0])
    m = len(board)
    result = []
    root = FindWordsTrie()

    def findWords(board, i, j, root):
        if i < 0 or i >= m or j < 0 or j <= n:
            return
        if board[i][j] == "$" or root.children[board[i][j]] == False:
            return

    for i in range(m):
        for j in range(n):
            ch = words[i][j]
            if root.children[ch]:
                findWords(board, i, j, root)
    return result


class StringIndicesTrie:
    def __init__(self):
        self.children = {}
        self.is_end = False
        self.count = 0


class StringTrie:
    def __init__(self):
        self.root = {}

    def insert(self, word):
        node = self.root
        for w in word:
            if w not in node.children:
                node.children[w] = StringIndicesTrie()
            node = node.children
        node.is_end = True
        node.count = len(word)

    def search(self, word):
        node = self.root
        for ch in word:
            if ch not in node.children:
                return False
            node = node.children[ch]
        return node.is_end

    def startsWith(self, prefix):
        node = self.root
        for ch in prefix:
            if ch not in node.children:
                return 0
            node = node.children[ch]
        return node.count


def stringIndices(wordsContainer, wordsQuery):
    stringsIndices = StringTrie()
    for word in wordsContainer:
        stringIndices.insert(word[::-1])


class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False
        self.index = -1


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word, i, wordsContainer):
        node = self.root
        for w in word[::-1]:
            if w not in node.children:
                node.children[w] = TrieNode()
            node = node.children[w]
            if node.index == -1 or len(wordsContainer[node.index]) > len(word):
                node.index = i
        node.is_end = True

    def search(self, words):
        node = self.root
        result_idx = node.index
        for i in range(len(words), -1, -1):
            if words[i] not in node.children:
                return result_idx
            result_idx = node.index
        return result_idx


def stringIndices(wordsContainer, wordsQuery):
    abc = Trie()
    result = []
    for i in range(len(wordsContainer)):
        abc.insert(wordsContainer[i], i, wordsContainer)

    for i in range(len(wordsQuery)):
        result.append(abc.search(wordsQuery[i]))
    return result
