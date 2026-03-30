class TrieNode:
    def __init__(self):
        self.is_end_of_word = False
        self.children = {}


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        crawl = self.root
        for char in word:
            if char not in crawl.children:
                crawl.children[char] = TrieNode()
            crawl = crawl.children[char]
        crawl.is_end_of_word = True

    def search(self, word: str) -> bool:
        crwal = self.root
        for char in word:
            if char not in crwal.children:
                return False
            crwal = crwal.children[char]
        return crwal.is_end_of_word

    def startsWith(self, prefix: str) -> bool:
        current_node = self.root
        for char in prefix:
            if char not in current_node.children:
                return False
            current_node = current_node.children[char]
        return True

    def delete(self, word):
        def _delete(current_node, word, depth):
            if depth == len(word):
                # Word found, set the end of word to False
                if not current_node.is_end_of_word:
                    return False  # Word not found
                current_node.is_end_of_word = False
                # If the current node has no other children, delete it
                return len(current_node.children) == 0

            char = word[depth]
            if char not in current_node.children:
                return False  # Word not found

            can_delete_child = _delete(current_node.children[char], word, depth + 1)

            if can_delete_child:
                # Remove the child node
                del current_node.children[char]
                # Return True if the current node can also be deleted
                return (
                    len(current_node.children) == 0 and not current_node.is_end_of_word
                )

            return False

        _delete(self.root, word, 0)


# Your Trie object will be instantiated and called as such:
# obj = Trie()
# obj.insert(word)
# param_2 = obj.search(word)
# param_3 = obj.startsWith(prefix)


from collections import defaultdict


class TrieRevision:
    def __init__(self):
        self.is_end_here = False
        self.children = defaultdict(TrieRevision)


class TrieClass:
    def __init__(self):
        self.node = TrieRevision()

    def insert(self, word):
        crawl = self.node
        for w in word:
            if w not in crawl.children:
                crawl.children[w] = TrieRevision()
            crawl = crawl.children[w]
        crawl.is_end_here = True

    def search(self, word):
        crawl = self.node
        for w in word:
            if w not in crawl.children:
                return False
            crawl = crawl.children[w]
        return crawl.is_end_here

    def startsWith(self, prefix):
        crawl = self.node
        for w in prefix:
            if w not in crawl.children:
                return False
            crawl = crawl.children[w]
        return True


import heapq


def meetingRoom2(start, end):
    arr = []
    if len(start) != len(end):
        return -1
    for i in range(len(start)):
        arr.append([start[i], end[i]])
    arr.sort(key=lambda x: x[0])
    # end_time = arr[0][1]
    # count = 1
    # for start, end in arr[1:]:
    #     if start >= end_time:
    #         end_time = max(end, end_time)
    #     else:
    #         count += 1
    # return count
    heap = []
    for start, end in arr:
        if heap and heap[0] <= start:
            heapq.heappop()
        heapq.heappush(end)
    return len(heap)


def minEatingSpeed(piles, h):
    start = 1
    end = max(piles)

    def canEat(mid):
        times = 0
        for p in piles:
            times += p // mid
            if p % mid != 0:
                times += 1
        return times <= h

    while start < end:
        mid = (end - start) // 2 + start
        if canEat(mid):
            end = mid
        else:
            start = mid + 1
    return end


def lowestCommonAncestor(root, p, q):
    if not root or root == p or root == q:
        return root
    left = lowestCommonAncestor(root.left, p, q)
    right = lowestCommonAncestor(root.right, p, q)
    if left and right:
        return root
    return left if left else right


def maxProductPath(grid):
    matrix = [[-1 for _ in range(len(grid[0]))] for _ in range(len(grid))]
    matrix[0][0] = [grid[0][0], grid[0][0]]
    mod = pow(10, 9) + 7
    for j in range(1, len(grid[0])):
        maxValue, minValue = matrix[0][j - 1]
        matrix[0][j] = [
            max(grid[0][j] * maxValue, grid[0][j] * minValue),
            min(grid[0][j] * maxValue, grid[0][j] * minValue),
        ]
    for i in range(1, len(grid)):
        maxValue, minValue = matrix[i - 1][0]
        matrix[i][0] = [
            max(grid[i][0] * maxValue, grid[i][0] * minValue),
            min(grid[i][0] * maxValue, grid[i][0] * minValue),
        ]
    for i in range(1, len(grid)):
        for j in range(1, len(grid[0])):
            maxValue, minValue = matrix[i - 1][j]
            maxValue1, minValue1 = matrix[i][j - 1]
            matrix[i][j] = [
                max(
                    grid[i][j] * maxValue,
                    grid[i][j] * minValue,
                    grid[i][j] * maxValue1,
                    grid[i][j] * minValue1,
                ),
                min(
                    grid[i][j] * maxValue,
                    grid[i][j] * minValue,
                    grid[i][j] * maxValue1,
                    grid[i][j] * minValue1,
                ),
            ]
    return (
        -1
        if max(matrix[len(grid) - 1][len(grid[0]) - 1]) < 0
        else max(matrix[len(grid) - 1][len(grid[0]) - 1]) % mod
    )


print(maxProductPath([[1, 3], [0, -4]]))
