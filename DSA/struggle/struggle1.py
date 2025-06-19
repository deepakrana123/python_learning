# import heapq


# def dfs(graph, word, visited):
#     visited[ord(word) - ord("a")] = 1
#     minChar = word
#     if word not in graph:
#         return word
#     for v in graph[word]:
#         if visited[ord(v) - ord("a")] == 0:
#             minChar = min(dfs(graph, v, visited), minChar)
#     return minChar


# def smallestEquivalentString(s1, s2, baseStr):
#     if len(s1) != len(s2):
#         return None
#     graph = {}
#     for i in range(len(s1)):
#         if s1[i] not in graph:
#             graph[s1[i]] = []
#         if s2[i] not in graph:
#             graph[s2[i]] = []
#         graph[s1[i]].append(s2[i])
#         graph[s2[i]].append(s1[i])

#     strs = ""

#     for word in baseStr:
#         visited = [0] * 26
#         strs += dfs(graph, word, visited)
#     return strs


# def answerString(word, numFriends):
#     n = len(word)
#     result = ""
#     longestPossible = n - numFriends + 1
#     for i in range(n):
#         canTakeLength = min(longestPossible, n - 1)
#         result = max(result, word[i:canTakeLength])
#     return result


# def sortedSquares(nums):
#     left = 0
#     right = len(nums) - 1
#     result = [0] * len(nums)
#     for i in range(len(nums)):
#         if abs(nums[left]) > abs(nums[right]):
#             result[i] = nums[left] ** 2
#             left += 1
#         else:
#             result[i] = nums[right] ** 2
#             right -= 1
#     return result[::-1]


# def findLeastNumOfUniqueInts(arr, k):
#     dicts = {}
#     for i in range(len(arr)):
#         dicts[arr[i]] = dicts.get(arr[i], 0) + 1
#     heap = []
#     for key in dicts:
#         heapq.heappush(heap, (dicts[key], key))
#     while k > 0:
#         a, b = heapq.heappop(heap)
#         if a - 1 != 0:
#             heapq.heappush(heap, (a - 1, b))
#         k -= 1
#     return len(heap)


# def commonChars(words):
#     dicts1 = {}
#     for w in words[0]:
#         dicts1[w] = dicts1.get(w, 0) + 1

#     for i in range(1, len(words)):
#         dicts2 = {}
#         for key in words[i]:
#             dicts2[key] = dicts2.get(key, 0) + 1
#         for w in dicts1:
#             if w in dicts2:
#                 dicts1[w] = min(dicts1[w], dicts2[w])
#             else:
#                 dicts1[w] = 0
#     abc = []
#     for key in dicts1:
#         if dicts1[key] != 0:
#             abc.append(key)
#     return abc


# def relativeSortArray(arr1, arr2):
#     dicts1 = {}
#     for w in arr1:
#         dicts1[w] = dicts1.get(w, 0) + 1
#     abc = []
#     for i in range(len(arr2)):
#         if arr2[i] in dicts1:
#             for _ in range(dicts1[arr2[i]]):
#                 abc.append(arr2[i])
#     return abc


# def heightChecker(heights):
#     expected = sorted(heights)
#     count = 0
#     for i in range(len(heights)):
#         if heights[i] != expected[i]:
#             count += 1
#     return count


# def buyChoco(prices, money):
#     prices.sort()
#     a = money - (prices[0] + prices[1])
#     if a >= 0:
#         return a
#     else:
#         return money


# def lastNonEmptyString(s):
#     seens = set()
#     stack = []
#     for word in s:
#         if word in seens:
#             stack.append(word)
#             break
#         seens.add(word)
#         stack.append(word)
#     target = ".".join(stack)
#     result = []
#     remove = False
#     i = 0
#     while i < len(s):
#         if not remove and s[i : i + len(target)] == target:
#             i += len(target)
#             remove = True
#         else:
#             result.append(s[i])
#             i += 1
#     return result


# def checkColumns(arr, col):
#     sums = 0
#     for i in range(len(arr)):
#         sums += arr[i][col]
#     return sums == 1


# def checkRows(arr, row):
#     sums = 0
#     for j in range(len(arr[0])):
#         sums += arr[row][j]
#     return sums == 1


# def numSpecial(mat):
#     count = 0
#     for i in range(len(mat)):
#         for j in range(len(mat[0])):
#             if mat[i][j] == 1:
#                 if checkColumns(mat, j) and checkRows(mat, i):
#                     count += 1
#     return count


# def lastNonEmptyString(s):
#     dicts = {}
#     dicts2 = {}
#     maxs = 0
#     for w in range(len(s)):
#         dicts[s[w]] = dicts.get(s[w], 0) + 1
#         maxs = max(dicts[s[w]], maxs)
#         dicts2[s[w]] = w
#     sts = ""
#     ab = set()
#     for key in dicts:
#         if dicts[key] == maxs:
#             ab.add(key)
#     for i in range(len(s) - 1, -1, -1):
#         if s[i] in ab and s[i] not in sts:
#             sts += s[i]
#             if len(sts) == len(ab):
#                 break
#     return sts[::-1]


# def returnToBoundaryCount(nums):
#     count = 0
#     sums = 0
#     for num in nums:
#         sums += num
#         if sums == 0:
#             count += 1
#     return count


# def numOfUnplacedFruits(fruits, baskets):
#     count = 0
#     for i in range(len(fruits)):
#         for j in range(len(baskets)):
#             if fruits[i] < baskets[j]:
#                 count += 1
#                 break
#     return len(fruits) - count if count > 0 else 0


# def arrayStringsAreEqual(word1, word2):
#     return "".join(word1) == "".join(word2)


# def largestGoodInteger(num):
#     count = -1
#     maxStr = ""
#     for i in range(2, len(num)):
#         if num[i - 1] == num[i] == num[i + 1]:
#             if count < int(num[i]):
#                 count = int(num[i])
#     for _ in range(3):
#         if count != -1:
#             maxStr += str(count)
#     return maxStr


# def numberOfSpecialChars(word):
#     lowers = set()
#     higher = set()
#     for w in word:
#         if w.islower():
#             lowers.add(w)
#         if w.isupper():
#             higher.add(w)
#     count = 0
#     for key in lowers:
#         if key.upper() in higher:
#             count += 1
#     return count


# # def getLargestOutlier(nums):
# def sortVowels(s):
#     arr = []
#     vowel = set("aeiouAEIOU")
#     t = list(s)
#     for i in range(len(s)):
#         if s[i] in vowel:
#             arr.append(s[i])
#     arr.sort()
#     j = 0
#     for i in range(len(s)):
#         if s[i] in vowel:
#             t[i] = arr[j]
#             j += 1
#     return "".join(t)


# def groupAnagrams(strs):
#     dicts = {}
#     for i in range(len(strs)):
#         rev = "".join(sorted(strs[i]))
#         if rev in dicts:
#             dicts[rev].append(strs[i])
#         else:
#             dicts[rev] = [strs[i]]
#     return list(dicts.values())


# def isPossibleDivide(nums, k):
#     if len(nums) % k != 0:
#         return False
#     dicts = {}
#     for num in nums:
#         dicts[num] = dicts.get(num, 0) + 1
#     # while dicts:
#     #     first_key = next(iter(sorted(dicts.items())))
#     #     for i in range(k):
#     #         value = first_key[0] + i
#     #         if value not in dicts or dicts[value] == 0:
#     #             return False
#     #         dicts[value] = dicts[value] - 1
#     #         if dicts[value] == 0:
#     #             del dicts[value]
#     # return True
#     for num in sorted(dicts):
#         if dicts[num] > 0:
#             freq = dicts[num]
#             for i in range(k):
#                 if dicts[num + i] < freq:
#                     return False
#                 dicts[num + i] -= freq
#     return True


# import heapq


# def clearStars(s):
#     stack = []
#     heap = []
#     deleted = set()
#     for i, ch in enumerate(s):
#         if ch != "*":
#             stack.append((s[i], i))
#             heapq.heappush(heap, (s[i], -i))
#         else:
#             while heap:
#                 char, index = heapq.heappop(heap)
#                 if -1 * index not in deleted:
#                     deleted.add(-1 * index)
#                     break
#     result = [char for char, indx in stack if indx not in deleted]
#     return "".join(result)


# from collections import deque


# def longestSubarray(nums, limit):
#     # result = 0
#     # for i in range(len(nums)):
#     #     count = 0
#     #     for j in range(i, len(nums)):
#     #         if abs(nums[i] - nums[j]) <= limit:
#     #             count += 1
#     #         else:
#     #             break
#     #     result = max(count, result)
#     # return result
#     max_d = deque()
#     min_d = deque()
#     left = 0
#     res = 0
#     for right in range(len(nums)):
#         while max_d and nums[right] > max_d[-1]:
#             max_d.pop()
#         while min_d and nums[right] < min_d[-1]:
#             min_d.pop()
#         max_d.append(nums[right])
#         min_d.append(nums[right])

#         while max_d[0] - min_d[0] > limit:
#             if nums[left] == max_d[0]:
#                 max_d.popleft()
#             if nums[left] == min_d[0]:
#                 min_d.popleft()
#             left += 1
#         res = max(right - left + 1, res)
#     return res


# def zeroFilledSubarray(nums):
#     i = 0
#     j = 0
#     result = 0
#     while j < len(nums):
#         if nums[j] != 0:
#             i = j + 1
#         result += j - i + 1
#         j += 1
#     return result


# def addSpaces(s, spaces):
#     i = 0
#     j = 0
#     strs = ""
#     while j < len(s):
#         if i < len(spaces) and spaces[i] < len(s) and j == spaces[i]:
#             strs += " "
#             i += 1
#         strs += s[j]
#         j += 1
#     return strs


# def maximizeGreatness(nums):
#     mins = min(nums)
#     count = 0
#     for i in range(len(nums)):
#         if nums[i] == mins:
#             count += 1
#     return len(nums) - count


# def buildArray(target, n):
#     i = 0
#     j = 0
#     arr = [i for i in range(1, n + 1)]
#     map = []
#     while j < len(arr):
#         map.append("Push")
#         if target[i] == arr[j]:
#             i += 1
#         else:
#             map.append("Pop")
#         j += 1
#     return map


# def maxVowels(s, k):
#     i = 0
#     j = 0
#     abc = set("aeiou")
#     result = 0
#     while j < len(s):
#         if s[i] in abc:
#             result = max(result, j - i + 1)
#             j += 1
#         else:
#             j += 1
#             i += 1
#     return result


# def maxDifference(s):
#     a1 = float("-inf")
#     a2 = float("inf")
#     dicts = {}
#     for key in s:
#         dicts[key] = dicts.get(key, 0) + 1
#     for key in s:
#         if dicts[key] % 2 == 0:
#             a2 = min(dicts[key], a2)
#         if dicts[key] % 2 != 0:
#             a1 = max(dicts[key], a1)
#     return a1 - a2


# def maxDiff(num):
#     a = str(num)
#     idx = next((i for i, c in enumerate(a) if c != "9"), -1)
#     b = ""
#     smallest = str(num)
#     if idx > -1:
#         b = a.replace(a[idx], "9")
#     else:
#         b = a
#     for i in range(len(a)):
#         ch = a[i]
#         if i == 0:
#             if ch != "1":
#                 smallest = a.replace(a[i], "1")
#                 break
#         elif ch != "0" and a[0] != ch:
#             smallest = a.replace(a[i], "0")
#             break
#     return int(b) - int(smallest)


# def leafSimilar(self, root1, root2):
#     arr1 = []
#     arr2 = []

#     def dfs(root1, arr):
#         if root1 == None:
#             return []
#         if root1.left == None and root1.right == None:
#             arr.append(root1.val)
#         dfs(root1.left, arr)
#         dfs(root1.right, arr)

#     dfs(root1, arr1)
#     dfs(root2, arr2)
#     return arr1 == arr2


# def evaluateTree(self, root):
#     def dfs(root):
#         if root == None:
#             return False
#         if root.left == None and root.right == None:
#             return root.val == 1

#         left_node = dfs(root.left)
#         right_node = dfs(root.right)
#         if root.val == 2:
#             return left_node or right_node
#         if root.val == 3:
#             return left_node and right_node

#     return dfs(root)


# from collections import deque


# def widthOfBinaryTree(self, root):
#     if root is None:
#         return 0
#     queue = [(root, 0)]
#     count = 0
#     while queue:
#         level_length = len(queue)
#         _, first_index = queue[0]
#         for i in range(level_length):
#             node, index = queue.pop(0)
#             index -= first_index
#             if node.left:
#                 queue.append((node.left, 2 * index + 1))
#             if node.right:
#                 queue.append((node.right, 2 * index + 2))
#         if queue:
#             count = max(count, queue[-1][1] - queue[0][1] + 1)
#         else:
#             count = max(count, 1)
#     return count


# def generateTree(head, left, right):
#     if left > right:
#         return None
#     mid = left + (right - left) / 2
#     root = TreeNode(head[mid])
#     root.left = generateTree(head[0:mid], left, right)
#     root.right = generateTree(head[mid + 1 : len(head)], left, right)
#     return root


# def sortedListToBST(self, head):
#     if head is None:
#         return None
#     arr = []
#     while head:
#         arr.append(head.val)
#         head = head.next
#     arr.append(head.val)
#     left = 0
#     right = len(arr)

#     return generateTree(arr, left, right)


# def buildTree(self, inorder: List[int], postorder: List[int]) -> Optional[TreeNode]:
#     self.postorderIndex = len(postorder) - 1
#     inorder_index_map = {val: i for i, val in enumerate(inorder)}

#     def build(left, right):
#         if left > right:
#             return None
#         root_val = postorder[self.preorderIndex]
#         root = TreeNode(root_val)
#         self.postorderIndex -= 1
#         root_index = inorder_index_map[root_val]
#         root.left = build(left, root_index - 1)
#         root.right = build(root_index + 1, right)
#         return root

#     return build(0, len(inorder) - 1)


# def buildTree(self, preorder, inorder):
#     self.preorderIndex = 0
#     inorder_index_map = {val: i for i, val in enumerate(inorder)}

#     def build(left, right):
#         if left > right:
#             return None
#         root_val = preorder[self.preorderIndex]
#         root = TreeNode(root_val)
#         self.preorderIndex += 1
#         root_index = inorder_index_map[root_val]
#         root.left = build(left, root_index - 1)
#         root.right = build(root_index + 1, right)
#         return root


#     return build(0, len(inorder) - 1)
# def addOneRow(self, root, val, depth):
# if depth == 1:
#     newRoot = TreeNode(val)
#     newRoot.left = root
#     return newRoot

# def dfs(root, currDepth):
#     if root is None:
#         return None
#     if currDepth - 1 == depth:
#         prevLeft = root.left
#         preRight = root.right
#         newNodeleft = TreeNode(val)
#         newNodeRight = TreeNode(val)
#         newNodeleft.left = prevLeft
#         newNodeRight.right = preRight
#         root.left = newNodeleft
#         root.right = newNodeRight
#     else:
#         dfs(root.left, currDepth + 1)
#         dfs(root.right, currDepth + 1)


def generateNodes(root, target):
    if root == None:
        return None

    generateNodes(root.left, target)
    generateNodes(root.right, target)
    if root.left == None and root.right == None and root.val == target:
        return None
    return root


def removeLeafNodes(root, target):
    return generateNodes(root, target)


def delNodes(self, root, to_delete):
    if root == None:
        return None


def trasverse(root, p, arr):
    if root is None:
        return False
    arr.append(root.val)
    if root.val == p:
        return True
    if trasverse(root.left, p, arr) or trasverse(root.right, p, arr):
        return True
    arr.pop()
    return False


def lowestCommonAncestor(root, p, q):
    arr1 = []
    arr2 = []
    trasverse(root, p, arr1)
    trasverse(root, q, arr2)
    i = 0
    i = 0
    while i < len(arr1) and i < len(arr2) and arr1[i] == arr2[i]:
        i += 1

    return arr1[i - 1]


def generate(root, result, curr):
    if root is None:
        return ""
    curr.append(root.val)
    if root.left == None and root.right == None:
        result.append(curr.copy())
    generate(root.left, result)
    generate(root.right, result)
    curr.pop()


# def maxAncestorDiff(root):
#     if root is None:
#         return 0
#     maxD=[0]
#     sumsVal()


def inorderRevesral(root, sum):
    if root is None:
        return None
    inorderRevesral(root.right, sum)
    sum[0] = sum[0] + root.val
    root.val = sum[0]
    inorderRevesral(root.left, sum)


def bstToGst(root):
    sum = [0]
    inorderRevesral(root, sum)
    return root


def bstToGst_iterative(root):
    stack = []
    node = root
    total = 0
    while stack or node:
        while node:
            stack.append(node)
            node = node.right
        node = stack.pop()
        total += node.val
        node.val = total
        node = node.left
    return root


def smallestFromLeaf(root):
    if root is None:
        return ""
    result = []
    generate(root, result)
    strs = []
    for path in result:
        s = "".join(chr(ord("a") + v) for v in reversed(path))
        strs.append(s)
    strs.sort()
    return strs[0] if strs else ""


def bstToGst(root):
    arr = []

    def inorder(root):
        if root is None:
            return None
        inorder(root.left)
        arr.append(root.val)
        inorder(root.right)

    sums = arr
    for i in range(len(arr) - 1, -1, -1):
        sums[i] = sums[i + 1] + sums[i]
    print(sums)


def divideArray(nums, k):
    nums.sort()
    if nums[1] - nums[0] > k:
        return []
    a = []
    i = 0
    while i < len(nums):
        if nums[i + 2] - nums[i] > k:
            return []
        a.append([nums[i], nums[i + 1], nums[i + 2]])
        i = i + 3
    return a


def partitionArray(nums, k):
    nums.sort()
    minVal = nums[0]
    count = 1
    for i in range(1, len(nums)):
        if nums[i] - minVal > k:
            count += 1
            minVal = nums[i]
    return count


print(partitionArray([3, 6, 1, 2, 5], k=2))
