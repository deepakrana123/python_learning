import heapq
from collections import deque


# # def dfs(graph, word, visited):
# #     visited[ord(word) - ord("a")] = 1
# #     minChar = word
# #     if word not in graph:
# #         return word
# #     for v in graph[word]:
# #         if visited[ord(v) - ord("a")] == 0:
# #             minChar = min(dfs(graph, v, visited), minChar)
# #     return minChar


# # def smallestEquivalentString(s1, s2, baseStr):
# #     if len(s1) != len(s2):
# #         return None
# #     graph = {}
# #     for i in range(len(s1)):
# #         if s1[i] not in graph:
# #             graph[s1[i]] = []
# #         if s2[i] not in graph:
# #             graph[s2[i]] = []
# #         graph[s1[i]].append(s2[i])
# #         graph[s2[i]].append(s1[i])

# #     strs = ""

# #     for word in baseStr:
# #         visited = [0] * 26
# #         strs += dfs(graph, word, visited)
# #     return strs


# # def answerString(word, numFriends):
# #     n = len(word)
# #     result = ""
# #     longestPossible = n - numFriends + 1
# #     for i in range(n):
# #         canTakeLength = min(longestPossible, n - 1)
# #         result = max(result, word[i:canTakeLength])
# #     return result


# # def sortedSquares(nums):
# #     left = 0
# #     right = len(nums) - 1
# #     result = [0] * len(nums)
# #     for i in range(len(nums)):
# #         if abs(nums[left]) > abs(nums[right]):
# #             result[i] = nums[left] ** 2
# #             left += 1
# #         else:
# #             result[i] = nums[right] ** 2
# #             right -= 1
# #     return result[::-1]


# # def findLeastNumOfUniqueInts(arr, k):
# #     dicts = {}
# #     for i in range(len(arr)):
# #         dicts[arr[i]] = dicts.get(arr[i], 0) + 1
# #     heap = []
# #     for key in dicts:
# #         heapq.heappush(heap, (dicts[key], key))
# #     while k > 0:
# #         a, b = heapq.heappop(heap)
# #         if a - 1 != 0:
# #             heapq.heappush(heap, (a - 1, b))
# #         k -= 1
# #     return len(heap)


# # def commonChars(words):
# #     dicts1 = {}
# #     for w in words[0]:
# #         dicts1[w] = dicts1.get(w, 0) + 1

# #     for i in range(1, len(words)):
# #         dicts2 = {}
# #         for key in words[i]:
# #             dicts2[key] = dicts2.get(key, 0) + 1
# #         for w in dicts1:
# #             if w in dicts2:
# #                 dicts1[w] = min(dicts1[w], dicts2[w])
# #             else:
# #                 dicts1[w] = 0
# #     abc = []
# #     for key in dicts1:
# #         if dicts1[key] != 0:
# #             abc.append(key)
# #     return abc


# # def relativeSortArray(arr1, arr2):
# #     dicts1 = {}
# #     for w in arr1:
# #         dicts1[w] = dicts1.get(w, 0) + 1
# #     abc = []
# #     for i in range(len(arr2)):
# #         if arr2[i] in dicts1:
# #             for _ in range(dicts1[arr2[i]]):
# #                 abc.append(arr2[i])
# #     return abc


# # def heightChecker(heights):
# #     expected = sorted(heights)
# #     count = 0
# #     for i in range(len(heights)):
# #         if heights[i] != expected[i]:
# #             count += 1
# #     return count


# # def buyChoco(prices, money):
# #     prices.sort()
# #     a = money - (prices[0] + prices[1])
# #     if a >= 0:
# #         return a
# #     else:
# #         return money


# # def lastNonEmptyString(s):
# #     seens = set()
# #     stack = []
# #     for word in s:
# #         if word in seens:
# #             stack.append(word)
# #             break
# #         seens.add(word)
# #         stack.append(word)
# #     target = ".".join(stack)
# #     result = []
# #     remove = False
# #     i = 0
# #     while i < len(s):
# #         if not remove and s[i : i + len(target)] == target:
# #             i += len(target)
# #             remove = True
# #         else:
# #             result.append(s[i])
# #             i += 1
# #     return result


# # def checkColumns(arr, col):
# #     sums = 0
# #     for i in range(len(arr)):
# #         sums += arr[i][col]
# #     return sums == 1


# # def checkRows(arr, row):
# #     sums = 0
# #     for j in range(len(arr[0])):
# #         sums += arr[row][j]
# #     return sums == 1


# # def numSpecial(mat):
# #     count = 0
# #     for i in range(len(mat)):
# #         for j in range(len(mat[0])):
# #             if mat[i][j] == 1:
# #                 if checkColumns(mat, j) and checkRows(mat, i):
# #                     count += 1
# #     return count


# # def lastNonEmptyString(s):
# #     dicts = {}
# #     dicts2 = {}
# #     maxs = 0
# #     for w in range(len(s)):
# #         dicts[s[w]] = dicts.get(s[w], 0) + 1
# #         maxs = max(dicts[s[w]], maxs)
# #         dicts2[s[w]] = w
# #     sts = ""
# #     ab = set()
# #     for key in dicts:
# #         if dicts[key] == maxs:
# #             ab.add(key)
# #     for i in range(len(s) - 1, -1, -1):
# #         if s[i] in ab and s[i] not in sts:
# #             sts += s[i]
# #             if len(sts) == len(ab):
# #                 break
# #     return sts[::-1]


# # def returnToBoundaryCount(nums):
# #     count = 0
# #     sums = 0
# #     for num in nums:
# #         sums += num
# #         if sums == 0:
# #             count += 1
# #     return count


# # def numOfUnplacedFruits(fruits, baskets):
# #     count = 0
# #     for i in range(len(fruits)):
# #         for j in range(len(baskets)):
# #             if fruits[i] < baskets[j]:
# #                 count += 1
# #                 break
# #     return len(fruits) - count if count > 0 else 0


# # def arrayStringsAreEqual(word1, word2):
# #     return "".join(word1) == "".join(word2)


# # def largestGoodInteger(num):
# #     count = -1
# #     maxStr = ""
# #     for i in range(2, len(num)):
# #         if num[i - 1] == num[i] == num[i + 1]:
# #             if count < int(num[i]):
# #                 count = int(num[i])
# #     for _ in range(3):
# #         if count != -1:
# #             maxStr += str(count)
# #     return maxStr


# # def numberOfSpecialChars(word):
# #     lowers = set()
# #     higher = set()
# #     for w in word:
# #         if w.islower():
# #             lowers.add(w)
# #         if w.isupper():
# #             higher.add(w)
# #     count = 0
# #     for key in lowers:
# #         if key.upper() in higher:
# #             count += 1
# #     return count


# # # def getLargestOutlier(nums):
# # def sortVowels(s):
# #     arr = []
# #     vowel = set("aeiouAEIOU")
# #     t = list(s)
# #     for i in range(len(s)):
# #         if s[i] in vowel:
# #             arr.append(s[i])
# #     arr.sort()
# #     j = 0
# #     for i in range(len(s)):
# #         if s[i] in vowel:
# #             t[i] = arr[j]
# #             j += 1
# #     return "".join(t)


# # def groupAnagrams(strs):
# #     dicts = {}
# #     for i in range(len(strs)):
# #         rev = "".join(sorted(strs[i]))
# #         if rev in dicts:
# #             dicts[rev].append(strs[i])
# #         else:
# #             dicts[rev] = [strs[i]]
# #     return list(dicts.values())


# # def isPossibleDivide(nums, k):
# #     if len(nums) % k != 0:
# #         return False
# #     dicts = {}
# #     for num in nums:
# #         dicts[num] = dicts.get(num, 0) + 1
# #     # while dicts:
# #     #     first_key = next(iter(sorted(dicts.items())))
# #     #     for i in range(k):
# #     #         value = first_key[0] + i
# #     #         if value not in dicts or dicts[value] == 0:
# #     #             return False
# #     #         dicts[value] = dicts[value] - 1
# #     #         if dicts[value] == 0:
# #     #             del dicts[value]
# #     # return True
# #     for num in sorted(dicts):
# #         if dicts[num] > 0:
# #             freq = dicts[num]
# #             for i in range(k):
# #                 if dicts[num + i] < freq:
# #                     return False
# #                 dicts[num + i] -= freq
# #     return True


# # import heapq


# # def clearStars(s):
# #     stack = []
# #     heap = []
# #     deleted = set()
# #     for i, ch in enumerate(s):
# #         if ch != "*":
# #             stack.append((s[i], i))
# #             heapq.heappush(heap, (s[i], -i))
# #         else:
# #             while heap:
# #                 char, index = heapq.heappop(heap)
# #                 if -1 * index not in deleted:
# #                     deleted.add(-1 * index)
# #                     break
# #     result = [char for char, indx in stack if indx not in deleted]
# #     return "".join(result)


# from collections import deque


# # def longestSubarray(nums, limit):
# #     # result = 0
# #     # for i in range(len(nums)):
# #     #     count = 0
# #     #     for j in range(i, len(nums)):
# #     #         if abs(nums[i] - nums[j]) <= limit:
# #     #             count += 1
# #     #         else:
# #     #             break
# #     #     result = max(count, result)
# #     # return result
# #     max_d = deque()
# #     min_d = deque()
# #     left = 0
# #     res = 0
# #     for right in range(len(nums)):
# #         while max_d and nums[right] > max_d[-1]:
# #             max_d.pop()
# #         while min_d and nums[right] < min_d[-1]:
# #             min_d.pop()
# #         max_d.append(nums[right])
# #         min_d.append(nums[right])

# #         while max_d[0] - min_d[0] > limit:
# #             if nums[left] == max_d[0]:
# #                 max_d.popleft()
# #             if nums[left] == min_d[0]:
# #                 min_d.popleft()
# #             left += 1
# #         res = max(right - left + 1, res)
# #     return res


# # def zeroFilledSubarray(nums):
# #     i = 0
# #     j = 0
# #     result = 0
# #     while j < len(nums):
# #         if nums[j] != 0:
# #             i = j + 1
# #         result += j - i + 1
# #         j += 1
# #     return result


# # def addSpaces(s, spaces):
# #     i = 0
# #     j = 0
# #     strs = ""
# #     while j < len(s):
# #         if i < len(spaces) and spaces[i] < len(s) and j == spaces[i]:
# #             strs += " "
# #             i += 1
# #         strs += s[j]
# #         j += 1
# #     return strs


# # def maximizeGreatness(nums):
# #     mins = min(nums)
# #     count = 0
# #     for i in range(len(nums)):
# #         if nums[i] == mins:
# #             count += 1
# #     return len(nums) - count


# # def buildArray(target, n):
# #     i = 0
# #     j = 0
# #     arr = [i for i in range(1, n + 1)]
# #     map = []
# #     while j < len(arr):
# #         map.append("Push")
# #         if target[i] == arr[j]:
# #             i += 1
# #         else:
# #             map.append("Pop")
# #         j += 1
# #     return map


# # def maxVowels(s, k):
# #     i = 0
# #     j = 0
# #     abc = set("aeiou")
# #     result = 0
# #     while j < len(s):
# #         if s[i] in abc:
# #             result = max(result, j - i + 1)
# #             j += 1
# #         else:
# #             j += 1
# #             i += 1
# #     return result


# # def maxDifference(s):
# #     a1 = float("-inf")
# #     a2 = float("inf")
# #     dicts = {}
# #     for key in s:
# #         dicts[key] = dicts.get(key, 0) + 1
# #     for key in s:
# #         if dicts[key] % 2 == 0:
# #             a2 = min(dicts[key], a2)
# #         if dicts[key] % 2 != 0:
# #             a1 = max(dicts[key], a1)
# #     return a1 - a2


# # def maxDiff(num):
# #     a = str(num)
# #     idx = next((i for i, c in enumerate(a) if c != "9"), -1)
# #     b = ""
# #     smallest = str(num)
# #     if idx > -1:
# #         b = a.replace(a[idx], "9")
# #     else:
# #         b = a
# #     for i in range(len(a)):
# #         ch = a[i]
# #         if i == 0:
# #             if ch != "1":
# #                 smallest = a.replace(a[i], "1")
# #                 break
# #         elif ch != "0" and a[0] != ch:
# #             smallest = a.replace(a[i], "0")
# #             break
# #     return int(b) - int(smallest)


# # def leafSimilar(self, root1, root2):
# #     arr1 = []
# #     arr2 = []

# #     def dfs(root1, arr):
# #         if root1 == None:
# #             return []
# #         if root1.left == None and root1.right == None:
# #             arr.append(root1.val)
# #         dfs(root1.left, arr)
# #         dfs(root1.right, arr)

# #     dfs(root1, arr1)
# #     dfs(root2, arr2)
# #     return arr1 == arr2


# # def evaluateTree(self, root):
# #     def dfs(root):
# #         if root == None:
# #             return False
# #         if root.left == None and root.right == None:
# #             return root.val == 1

# #         left_node = dfs(root.left)
# #         right_node = dfs(root.right)
# #         if root.val == 2:
# #             return left_node or right_node
# #         if root.val == 3:
# #             return left_node and right_node

# #     return dfs(root)


# # from collections import deque


# # def widthOfBinaryTree(self, root):
# #     if root is None:
# #         return 0
# #     queue = [(root, 0)]
# #     count = 0
# #     while queue:
# #         level_length = len(queue)
# #         _, first_index = queue[0]
# #         for i in range(level_length):
# #             node, index = queue.pop(0)
# #             index -= first_index
# #             if node.left:
# #                 queue.append((node.left, 2 * index + 1))
# #             if node.right:
# #                 queue.append((node.right, 2 * index + 2))
# #         if queue:
# #             count = max(count, queue[-1][1] - queue[0][1] + 1)
# #         else:
# #             count = max(count, 1)
# #     return count


# # def generateTree(head, left, right):
# #     if left > right:
# #         return None
# #     mid = left + (right - left) / 2
# #     root = TreeNode(head[mid])
# #     root.left = generateTree(head[0:mid], left, right)
# #     root.right = generateTree(head[mid + 1 : len(head)], left, right)
# #     return root


# # def sortedListToBST(self, head):
# #     if head is None:
# #         return None
# #     arr = []
# #     while head:
# #         arr.append(head.val)
# #         head = head.next
# #     arr.append(head.val)
# #     left = 0
# #     right = len(arr)

# #     return generateTree(arr, left, right)


# # def buildTree(self, inorder: List[int], postorder: List[int]) -> Optional[TreeNode]:
# #     self.postorderIndex = len(postorder) - 1
# # #     inorder_index_map = {val: i for i, val in enumerate(inorder)}

# # #     def build(left, right):
# # #         if left > right:
# # #             return None
# # #         root_val = postorder[self.preorderIndex]
# # #         root = TreeNode(root_val)
# # #         self.postorderIndex -= 1
# # #         root_index = inorder_index_map[root_val]
# # #         root.left = build(left, root_index - 1)
# # #         root.right = build(root_index + 1, right)
# # #         return root

# # #     return build(0, len(inorder) - 1)


# # # def buildTree(self, preorder, inorder):
# # #     self.preorderIndex = 0
# # #     inorder_index_map = {val: i for i, val in enumerate(inorder)}

# # #     def build(left, right):
# # #         if left > right:
# # #             return None
# # #         root_val = preorder[self.preorderIndex]
# # #         root = TreeNode(root_val)
# # #         self.preorderIndex += 1
# # #         root_index = inorder_index_map[root_val]
# # #         root.left = build(left, root_index - 1)
# # #         root.right = build(root_index + 1, right)
# # #         return root


# # #     return build(0, len(inorder) - 1)
# # # def addOneRow(self, root, val, depth):
# # # if depth == 1:
# # #     newRoot = TreeNode(val)
# # #     newRoot.left = root
# # #     return newRoot

# # # def dfs(root, currDepth):
# # #     if root is None:
# # #         return None
# # #     if currDepth - 1 == depth:
# # #         prevLeft = root.left
# # #         preRight = root.right
# # #         newNodeleft = TreeNode(val)
# # #         newNodeRight = TreeNode(val)
# # #         newNodeleft.left = prevLeft
# # #         newNodeRight.right = preRight
# # #         root.left = newNodeleft
# # #         root.right = newNodeRight
# # #     else:
# # #         dfs(root.left, currDepth + 1)
# # #         dfs(root.right, currDepth + 1)


# # def generateNodes(root, target):
# #     if root == None:
# #         return None

# #     generateNodes(root.left, target)
# #     generateNodes(root.right, target)
# #     if root.left == None and root.right == None and root.val == target:
# #         return None
# #     return root


# # def removeLeafNodes(root, target):
# #     return generateNodes(root, target)


# # def delNodes(self, root, to_delete):
# #     if root == None:
# #         return None


# # def trasverse(root, p, arr):
# #     if root is None:
# #         return False
# #     arr.append(root.val)
# #     if root.val == p:
# #         return True
# #     if trasverse(root.left, p, arr) or trasverse(root.right, p, arr):
# #         return True
# #     arr.pop()
# #     return False


# # def lowestCommonAncestor(root, p, q):
# #     arr1 = []
# #     arr2 = []
# #     trasverse(root, p, arr1)
# #     trasverse(root, q, arr2)
# #     i = 0
# #     i = 0
# #     while i < len(arr1) and i < len(arr2) and arr1[i] == arr2[i]:
# #         i += 1

# #     return arr1[i - 1]


# # def generate(root, result, curr):
# #     if root is None:
# #         return ""
# #     curr.append(root.val)
# #     if root.left == None and root.right == None:
# #         result.append(curr.copy())
# #     generate(root.left, result)
# #     generate(root.right, result)
# #     curr.pop()


# # # def maxAncestorDiff(root):
# # #     if root is None:
# # #         return 0
# # #     maxD=[0]
# # #     sumsVal()


# # def inorderRevesral(root, sum):
# #     if root is None:
# #         return None
# #     inorderRevesral(root.right, sum)
# #     sum[0] = sum[0] + root.val
# #     root.val = sum[0]
# #     inorderRevesral(root.left, sum)


# # def bstToGst(root):
# #     sum = [0]
# #     inorderRevesral(root, sum)
# #     return root


# # def bstToGst_iterative(root):
# #     stack = []
# #     node = root
# #     total = 0
# #     while stack or node:
# #         while node:
# #             stack.append(node)
# #             node = node.right
# #         node = stack.pop()
# #         total += node.val
# #         node.val = total
# #         node = node.left
# #     return root


# # def smallestFromLeaf(root):
# #     if root is None:
# #         return ""
# #     result = []
# #     generate(root, result)
# #     strs = []
# #     for path in result:
# #         s = "".join(chr(ord("a") + v) for v in reversed(path))
# #         strs.append(s)
# #     strs.sort()
# #     return strs[0] if strs else ""


# # def bstToGst(root):
# #     arr = []

# #     def inorder(root):
# #         if root is None:
# #             return None
# #         inorder(root.left)
# #         arr.append(root.val)
# #         inorder(root.right)

# #     sums = arr
# #     for i in range(len(arr) - 1, -1, -1):
# #         sums[i] = sums[i + 1] + sums[i]
# #     print(sums)


# # def divideArray(nums, k):
# #     nums.sort()
# #     if nums[1] - nums[0] > k:
# #         return []
# #     a = []
# #     i = 0
# #     while i < len(nums):
# #         if nums[i + 2] - nums[i] > k:
# #             return []
# #         a.append([nums[i], nums[i + 1], nums[i + 2]])
# #         i = i + 3
# #     return a


# # def partitionArray(nums, k):
# #     nums.sort()
# #     minVal = nums[0]
# #     count = 1
# #     for i in range(1, len(nums)):
# #         if nums[i] - minVal > k:
# #             count += 1
# #             minVal = nums[i]
# #     return count


# # def maxDistance(s, k):
# #     south = 0
# #     north = 0
# #     west = 0
# #     east = 0
# #     maxD = 0
# #     distance = 0
# #     for i in range(len(s)):
# #         if s[i] == "E":
# #             east += 1
# #         if s[i] == "W":
# #             west += 1
# #         if s[i] == "N":
# #             north += 1
# #         if s[i] == "S":
# #             south += 1
# #         currMan = abs(north - south) + abs(east - west)
# #         distance = i + 1
# #         wasted = distance - currMan
# #         usedK = 0
# #         if wasted != 0:
# #             usedK = min(wasted, k * 2)
# #         maxD = max(maxD, currMan + usedK)

# #     return maxD


# # def isCompleteTree(root):
# #     if root is None:
# #         return 0
# #     queue = deque([root])
# #     flag = False
# #     while queue:
# #         node = queue.popLeft()
# #         if node is None:
# #             flag = True
# #         else:
# #             if flag:
# #                 return True
# #         queue.append((node.left))
# #         queue.append((node.right))
# #     return True


# # def convertTreeToGraph(self, root, val, dicts):
# #     if root is None:
# #         return
# #     if root.val not in dicts:
# #         dicts[root.val] = set()
# #     adjancent_list = dicts[root.val]
# #     if val != 0:
# #         adjancent_list.add(val)
# #     if root.left:
# #         adjancent_list.add(root.left.val)
# #     if root.right:
# #         adjancent_list.add(root.right.val)
# #     convertTreeToGraph(root.left, root.val, dicts)
# #     convertTreeToGraph(root.right, root.val, dicts)


# # def amountOfTime(self, root, start):
# #     tree_map  = {}
# #     self.convertTreeToGraph(root, 0, tree_map)
# #     queue = deque([start])
# #     minute = 0
# #     visited = {start}
# #     while queue:
# #         level_size = len(queue)
# #         while level_size:
# #             node = queue.popleft()
# #             for node in tree_map:
# #                 if node not in visited:
# #                     visited.add(node)
# #                     queue.append(node)
# #             level_size -= 1
# #         minute += 1
# #     return minute - 1


# # # Definition for a binary tree node.
# # # class TreeNode:
# # #     def __init__(self, x):
# # #         self.val = x
# # #         self.left = None
# # #         self.right = None


# # class Solution:
# #     def convertTreeToGraph(self, root, val, dicts):
# #         if root is None:
# #             return
# #         if root.val not in dicts:
# #             dicts[root.val] = set()
# #         adjancent_list = dicts[root.val]
# #         if val != 0:
# #             adjancent_list.add(val)
# #             dicts[val].add(root.val)
# #         if root.left:
# #             adjancent_list.add(root.left.val)
# #         if root.right:
# #             adjancent_list.add(root.right.val)
# #         self.convertTreeToGraph(root.left, root.val, dicts)
# #         self.convertTreeToGraph(root.right, root.val, dicts)

# #     def inorder(self, root, tree_map):
# #         if root is None:
# #             return

# #         if root.left is not None:
# #             tree_map[root.left] = root
# #         self.inorder(root.left)
# #         if root.right is not None:
# #             tree_map[root.right] = root
# #         self.inorder(root.right)

# #     def distanceK(self, root: TreeNode, target: TreeNode, k: int) -> List[int]:
# #         tree_map: Dict[int, Set[int]] = {}
# #         # self.convertTreeToGraph(root, 0, tree_map)
# #         self.inorder(root, tree_map)
# #         queue = deque([target])
# #         result = []
# #         visited = {target.val}
# #         while queue:
# #             level_size = len(queue)
# #             if k == 0:
# #                 break
# #             while level_size:
# #                 curr = queue.popleft()
# #                 if curr.left is not None and curr.left.val not in visited:
# #                     queue.append(curr.left)
# #                     visited.add(curr.left.val)
# #                 if curr.right is not None and curr.right.val not in visited:
# #                     queue.append(curr.right)
# #                     visited.add(curr.right.val)
# #                 if tree_map[curr] and tree_map[curr].val not in visited:
# #                     queue.append(tree_map[curr])
# #                     visited.add(tree_map[curr].val)
# #                 level_size -= 1
# #             k -= 1
# #         while queue:
# #             temp = queue.popleft()
# #             result.append(temp.val)
# #         return result


# # def minimumDeletions(word, k):
# #     dicts = [0] * 26
# #     for w in word:
# #         dicts[ord(w) - ord("a")] = dicts[ord(w) - ord("a")] + 1
# #     dicts.sort()
# #     cumilutive_del = 0
# #     result = len(word)
# #     for i in range(26):
# #         delete = cumilutive_del
# #         for j in range(25, -1, -1):
# #             if dicts[j] - dicts[i] <= k:
# #                 break
# #             delete += abs(dicts[j] - dicts[i] - k)
# #         result = min(result, delete)
# #         cumilutive_del += dicts[i]
# #     return result

# #     # for i in range(26):
# #     #     for j in range(25, -1, -1):
# #     #         if j > i:
# #     #             break
# #     # for i in range(26):
# #     #     delete = 0
# #     #     for j in range(26):
# #     #         if i == j:
# #     #             continue
# #     #         if dicts[j] < dicts[i]:
# #     #             delete += dicts[j]
# #     #         elif abs(dicts[j] - dicts[i]) > k:
# #     #             delete += abs(dicts[j] - dicts[i] - k)
# #     #     result = min(delete, result)
# #     # return result


# def divideString(s, k, fill):
#     a = len(s) // k
#     c = len(s) - a * k
#     i = 0
#     result = []
#     while i < len(s) - c:
#         result.append(s[i : i + k])
#         i = i + k

#     ac = s[i::]
#     sa = ac
#     for i in range(k - len(s[i::])):
#         sa += "x"
#     if ac:
#         result.append(sa)
#     return result


# class Solution:
#     def longestZigZag(self, root):
#         self.maxLength = 0

#         def solve(root, left, right):
#             if root is None:
#                 return
#             self.maxLength = max(self.maxLength, left, right)
#             solve(root.left, right + 1, 0)
#             solve(root.right, 0, left + 1)

#         # def solve(root, steps, goLeft):
#         #     if root is None:
#         #         return
#         #     self.maxLength = max(self.maxLength, steps)
#         #     if goLeft:
#         #         solve(root.left, steps + 1, False)
#         #         solve(root.right, 1, True)
#         #     else:
#         #         solve(root.right, steps + 1, False)
#         #         solve(root.left, 1, True)

#         # solve(root, 0, True)
#         # solve(root, 0, False)
#         solve(root, 0, 0)
#         return self.maxLength


# def __init__(self, val=0, left=None, right=None):
#     self.val = val
#     self.left = left
#     self.right = right


# class Solution:
#     def isPlaindrome(self, num):
#         i = 0
#         j = len(num) - 1
#         while i < j:
#             if num[i] != num[j]:
#                 return False
#             i += 1
#             j -= 1
#         return True

#     def convertToBaseK(self, num, k):
#         if num == 0:
#             return "0"
#         res = ""
#         while num > 0:
#             res += str(num % k)
#             num //= k
#         return res

#     def kMirror(self, k: int, n: int) -> int:
#         sums = 0
#         l = 1
#         while n > 0:
#             half_length = (l + 1) // 2
#             min_num = 10 ** (half_length - 1)
#             max_num = 10**half_length - 1
#             for num in range(min_num, max_num + 1):
#                 first_half = str(num)
#                 second_half = "".join(reversed(first_half))
#                 pal = ""
#                 if l % 2 == 0:
#                     pal = first_half + second_half
#                 else:
#                     pal = first_half + second_half[1:]
#                 pal_num = int(pal)
#                 baseK = self.convertToBaseK(pal_num, k)
#                 if self.isPlaindrome(baseK):
#                     sums += pal_num
#                     n -= 1
#                     if n == 0:
#                         break
#             l += 1
#         return sums


# def findKDistantIndices(nums, key, k):
#     arr = []
#     for i in range(len(nums)):
#         if nums[i] == key:
#             arr.append(i)
#     result = set()
#     for i in range(len(nums)):
#         for j in arr:
#             if abs(i - j) <= k:
#                 result.add(nums[i])
#     return result


# def findCount(nums1, nums2, target):
#     productCount = 0
#     n = len(nums2)
#     for i in range(len(nums1)):
#         if nums1[i] >= 0:
#             l = 0
#             r = n - 1
#             m = -1
#             while l <= r:
#                 mid = l + (r - l) // 2
#                 prod = nums1[i] * nums2[mid]
#                 if prod <= target:
#                     m = mid
#                     l = mid + 1
#                 else:
#                     r = mid - 1
#             productCount += m + 1

#         else:
#             l = 0
#             r = n - 1
#             m = n
#             while l <= r:
#                 mid = l + (r - l) // 2
#                 prod = nums1[i] * nums2[mid]
#                 if prod <= target:
#                     m = mid
#                     l = mid + 1
#                 else:
#                     r = mid - 1
#             productCount += n - m
#     return productCount


# def kthSmallestProduct(nums1, nums2, k):
#     result = 0
#     l = -(10**10)
#     r = 10**10
#     while l <= r:
#         mid = l + (r - l) // 2
#         countSmallest = findCount(nums1, nums2, mid)
#         if countSmallest >= k:
#             result = mid
#             r = mid - 1
#         else:
#             l = mid + 1
#     return result


# class Solution:
#     # def solve(self, root, moves):
#     #     if root is None:
#     #         return 0
#     #     left = self.solve(root.left, moves)
#     #     right = self.solve(root.right, moves)
#     #     moves[0] = moves[0] + left + right
#     #     return abs(left + right) + root.val - 1

#     # def distributeCoins(self, root):
#     #     moves = [0]
#     #     return self.solve(root, moves)

#     # def solve(self, root, maxx):
#     #     if root is None:
#     #         return (0, 0)
#     #     leftsum, leftcount = self.solve(root.left, maxx)
#     #     rightsum, rightcount = self.solve(root.right, maxx)
#     #     total_sum = root.val + leftsum + rightsum
#     #     total_count = 1 + leftcount + rightcount
#     #     maxx = max(maxx, total_sum // total_count)
#     #     return (total_sum, total_count)

#     # def averageOfSubtree(self, root):
#     #     self.max = float("-inf")
#     #     self.solvetree(root, self.max)
#     #     return self.max


#     def createBinaryTree(descriptions):
#         mp = {}
#         childAlready = []
#         for parent, child, move in descriptions:
#             if parent not in mp:
#                 mp[parent] = TreeNode(parent)
#             if child not in mp:
#                 mp[child] = TreeNode(child)
#             childAlready.append(child)
#         for parent, child, move in descriptions:
#             if move == 1:
#                 mp[parent].left = mp[child]
#             if move == 0:
#                 mp[parent].right = mp[child]
# def longestSubsequence(s, k):
#  start with zero and and do o/1 knapsack
#     length = 0
#     powervalue = 1
#     for i in range(len(s) - 1, -1, -1):
#         if s[i] == "0":
#             length += 1
#         elif powervalue <= k:
#             k = k - powervalue
#             length += 1
#         if powervalue <= k:
#             powervalue *= 2
#     return length


# def convertTreeToGraph(self, root, val, dicts):
#     # if root is None:
#     #     return
#     # if root.val not in dicts:
#     #     dicts[root.val] = set()
#     # adjancent_list = dicts[root.val]
#     # if val != 0:
#     #     adjancent_list.add(val)
#     # if root.left:
#     #     adjancent_list.add(root.left.val)
#     # if root.right:
#     #     adjancent_list.add(root.right.val)
#     # self.convertTreeToGraph(root.left, root.val, dicts)
#     # self.convertTreeToGraph(root.right, root.val, dicts)
#     if root is None:
#         return
#     if root.val != 0:
#         dicts[root.val] = set()
#     adjancent_list = dicts[root.val]
#     if val != 0:
#         adjancent_list.add(val)
#     if root.left != None:
#         adjancent_list.add(root.left.val)
#     if root.right != None:
#         adjancent_list.add(root.right.val)
#     self.convertTreeToGraph(root.left, root.val, dicts)
#     self.convertTreeToGraph(root.right, root.val, dicts)


# def amountOfTime(self, root, start):
#     tree_map = {}
#     self.convertTreeToGraph(root, 0, tree_map)
#     queue = deque()
#     queue.append([start])
#     visited = set()
#     visited.add(start)
#     mintue = 0
#     while queue:
#         length = len(queue)
#         for i in range(length):
#             node = queue.popleft()
#             if node not in visited:
#                 queue.append(node)
#                 visited.add(node)
#         mintue += 1
#     return mintue - 1


# # optimial ways to calculate ncr
# # go for pascal triangle
# class Solution:

#     def solve(self, nums):
#         if self.size < 3:
#             return 1
#         leftArr = []
#         rightArr = []
#         for i in range(1, len(nums)):
#             if nums[i] < nums[0]:
#                 leftArr.append(nums[i])
#             else:
#                 rightArr.append(nums[i])
#         x = self.solve(leftArr) % self.mod
#         y = self.solve(rightArr) % self.mod
#         z = self.pascalTriangle[self.size - 1][len(leftArr) - 1]
#         return x * y * z

#     def numOfWays(self, nums):
#         self.size = len(nums)
#         self.mod = pow(10, 9) + 7
#         self.pascalTriangle = [
#             [1 for _ in range(self.size + 1)] for _ in range(self.size + 1)
#         ]
#         for i in range(self.size + 1):
#             for j in range(1, self.size):
#                 self.pascalTriangle[i][j] = (
#                     self.pascalTriangle[i - 1][j] + self.pascalTriangle[i - 1][j - 1]
#                 ) % self.mod

#         return self.solve(nums) - 1


# #  diameter of tree or grap is take a random node and find the farthest node form that particular node , and reprocess form that to find the farthest node form that particular node
# # class Solution:
# #     def bfs(adj, start):
# #         queue = deque(start)
# #         visited = set()
# #         visited.add(start)
# #         distance = 0
# #         farthestNode = start
# #         while queue:
# #             length = len(queue)
# #             while length > 0:
# #                 node = queue.popleft()
# #                 farthestNode = node
# #                 if node in visited:
# #                     queue.append(node)
# #                     visited.add(node)
# #                 length -= 1
# #             if queue:
# #                 distance += 1
# #         return {farthestNode, distance}

# #     def findDiameter(adj):
# #         farthestNode, dist = bfs(adj, 0)
# #         secondfarthestNode, dist1 = bfs(adj, farthestNode)
# #         return dist1

# #     def buildAdj(edges):
# #         tree_map = {}
# #         for edge in edges:
# #             u = edge[0]
# #             v = edge[v]
# #             tree_map[u].append(v)
# #             tree_map[v].append(u)
# #         return tree_map

# #     def minimumDiameterAfterMerge(edges1, edges2):
# #         tree_map = buildAdj(edges1)
# #         tree_map1 = buildAdj(edges2)
# #         d1 = findDiameter(adj1)
# #         d2 = findDiameter(adj2)
# #         combined = (d1 + 1) // 2 + (d2 + 1) // 2 + 1
# #         return max(combined, d1, d2)


# from collections import deque, defaultdict
# import math


# class Solution:
#     def bfs(self, adj, start):
#         queue = deque([start])
#         visited = set([start])
#         distance = {start: 0}
#         farthest_node = start

#         while queue:
#             node = queue.popleft()
#             for neighbor in adj[node]:
#                 if neighbor not in visited:
#                     visited.add(neighbor)
#                     distance[neighbor] = distance[node] + 1
#                     queue.append(neighbor)
#                     if distance[neighbor] > distance[farthest_node]:
#                         farthest_node = neighbor

#         return farthest_node, distance[farthest_node]

#     def findDiameter(self, adj):
#         far_node, _ = self.bfs(adj, next(iter(adj)))
#         farthest_node, dist = self.bfs(adj, far_node)
#         return dist

#     def buildAdj(self, edges):
#         tree_map = defaultdict(list)
#         for u, v in edges:
#             tree_map[u].append(v)
#             tree_map[v].append(u)
#         return tree_map

#     def minimumDiameterAfterMerge(self, edges1, edges2):
#         tree_map1 = self.buildAdj(edges1)
#         tree_map2 = self.buildAdj(edges2)
#         d1 = self.findDiameter(tree_map1)
#         d2 = self.findDiameter(tree_map2)
#         combined = math.ceil(d1 / 2) + math.ceil(d2 / 2) + 1
#         return max(d1, d2, combined)


# # def buildSequence(s,sets,k):

# # def longestSubsequenceRepeatedK(s, k):
# #     longestSubSequence = len(s) // k
# #     dicts = {}
# #     sets = set()
# #     for value in s:
# #         dicts[value] = dicts.get(value, 0) + 1
# #     for key in dicts:
# #         if dicts[key] >= k:
# #             sets.add(key)

# #     buildSequence(s,sets,k)
# #     print(sets)


# # print(longestSubsequenceRepeatedK("letsleetcode", k=2))
# class Solution:
#     def numSubseq(self, nums, target):
#         left = 0
#         right = len(nums) - 1
#         nums.sort()
#         result = 0
#         while left <= right:
#             if nums[right] + nums[left] <= target:
#                 result = result + 2 ** (right - left)
#                 left += 1
#             else:
#                 right -= 1
#         return result

#     def recoverFromPreorder(self, traversal: str):
#         i = 0
#         depth = 0
#         n = len(traversal)

#         def solve(currIndex, traversal, depth, n):
#             if currIndex > n:
#                 return None
#             j = 0
#             while j < n and traversal[j] == "_":
#                 j += 1
#             dash = j - currIndex
#             if dash != depth:
#                 return None
#             currIndex = dash + currIndex
#             num = 0
#             while currIndex < n and traversal[currIndex].isdigit():
#                 num = num * 10 + int(traversal[currIndex])
#             root = TreeNode(num)
#             root.left = solve(currIndex, traversal, depth + 1, n)
#             root.right = solve(currIndex, traversal, depth + 1, n)
#             return root

#         return solve(i, traversal, depth, n)


def possibleStringCount(word):
    result = 0
    for i in range(1, len(word)):
        if word[i] == word[i - 1]:
            result += 1
    return result + 1


print(possibleStringCount("abbcccc"))


class Solution:
    def solve(self, freq, index, k, result):
        if len(freq) <= index:
            if result < k:
                return 1
            return 0
        count = 0
        for take in range(len(freq[index])):
            if count + take < k:
                result = (
                    result + self.solve(freq, k, index + 1, k, count + take)
                ) % self.mod
            else:
                break
        return result

    def possibleStringCount(self, word, k):
        freq = []
        count = 1
        self.mod = pow(10, 9) + 7
        if len(word) < k:
            return 0
        for i in range(1, len(word)):
            if word[i] == word[i - 1]:
                count += 1
            else:
                freq.append(count)
                count = 1
        dp = [[-1 for _ in range(len(freq))] for _ in range(len(freq))]
        freq.append(count)
        p = 1
        for f in freq:
            p = (p * f) % self.mod
        if len(freq) >= k:
            return p
        invalidCount = self.solve(freq, 0, k, 0)
        return p - invalidCount


def reverseAndAdd(s):
    result = ""
    for char in s:
        result += chr(ord(char) + 1)
    return result


def kthCharacter(self, k):
    if k < 0:
        return ""
    w = "a"
    if k == 1:
        return w
    while k > 1:
        w = w + reverseAndAdd(w)
        if len(w) > k:
            return w[k]
        k - 1
    return ""


def helper(n, memo):
    if n == 0:
        return 0
    if n in memo:
        return memo[n]
    minCount = float("inf")
    i = 1
    while i * i <= n:
        result = 1 + helper(n - i * i)
        minCount = min(result, minCount)
        i += 1
    memo[n] = minCount
    return minCount


def numSquares(n):
    # return helper(n, {})
    if n <= 0:
        return 0
    square = [i * i for i in range(1, int(n**0.5) + 1)]
    queue = deque([(0, 0)])

    visited = set()
    while queue:
        total, steps = queue.popleft()
        for sq in square:
            next_total = total + sq
            if next_total == n:
                return steps + 1
            if next_total < n and next_total not in visited:
                visited.add(next_total)
                queue.append((next_total, steps + 1))
    return -1


def dfs(grid, i, j):
    if i >= len(grid) or j >= len(grid[0]) or i < 0 or j < 0:
        return False
    if grid[i][j] == 1:
        return True
    grid[i][j] = 2
    return (
        dfs(grid, i - 1, j)
        and dfs(grid, i + 1, j)
        and dfs(grid, i, j - 1)
        and dfs(grid, i, j + 1)
    )


def closedIsland(grid):
    m, n = len(grid), len(grid[0])
    count = 0
    for i in range(m):
        for j in range(n):
            if grid[i][j] == 0:
                if dfs(grid, i, j):
                    count += 1
    return count


from collections import deque


def maximumSafenessFactor(grid):
    n = len(grid)
    dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    # Step 1: Multi-source BFS to compute distance from each cell to nearest thief
    distanceNearestThief = [[-1] * n for _ in range(n)]
    visited = [[False] * n for _ in range(n)]
    queue = deque()

    for i in range(n):
        for j in range(n):
            if grid[i][j] == 1:
                queue.append((i, j))
                visited[i][j] = True
                distanceNearestThief[i][j] = 0

    level = 0
    while queue:
        for _ in range(len(queue)):
            x, y = queue.popleft()
            for dx, dy in dirs:
                nx, ny = x + dx, y + dy
                if 0 <= nx < n and 0 <= ny < n and not visited[nx][ny]:
                    visited[nx][ny] = True
                    distanceNearestThief[nx][ny] = level + 1
                    queue.append((nx, ny))
        level += 1

    # Step 2: Binary search over safeness factor
    def check(mid_sf):
        que = deque([(0, 0)])
        visited = set()
        visited.add((0, 0))
        if distanceNearestThief[0][0] < mid_sf:
            return False

        while que:
            x, y = que.popleft()
            if x == n - 1 and y == n - 1:
                return True
            for dx, dy in dirs:
                nx, ny = x + dx, y + dy
                if (
                    0 <= nx < n
                    and 0 <= ny < n
                    and (nx, ny) not in visited
                    and distanceNearestThief[nx][ny] >= mid_sf
                ):
                    visited.add((nx, ny))
                    que.append((nx, ny))
        return False

    l = 0
    r = max(max(row) for row in distanceNearestThief)
    result = 0
    while l <= r:
        mid = (l + r) // 2
        if check(mid):
            result = mid
            l = mid + 1
        else:
            r = mid - 1
    return result


from collections import deque


def snakesAndLadders(board):
    n = len(board)
    visited = [[False for _ in range(n)] for _ in range(n)]
    queue = deque()
    queue.append(1)  # Start from square 1
    steps = 0

    def getCord(val):
        rowFromBottom = (val - 1) // n
        row = n - 1 - rowFromBottom
        col = (val - 1) % n
        if rowFromBottom % 2 == 1:
            col = n - 1 - col
        return row, col

    while queue:
        for _ in range(len(queue)):
            x = queue.popleft()
            if x == n * n:
                return steps
            for move in range(1, 7):
                next_val = x + move
                if next_val > n * n:
                    continue
                r, c = getCord(next_val)
                if visited[r][c]:
                    continue
                visited[r][c] = True
                if board[r][c] == -1:
                    queue.append(next_val)
                else:
                    queue.append(board[r][c])
        steps += 1

    return -1


def dfs(ancestor, adj, currNode, result):
    pass
    # for ngbr in adj[currNode]:
    #     if result[ngbr]


def getAncestors(n, edges):
    adj = defaultdict(list)
    indegree = [0] * n
    for u, v in edges:
        adj[u].append(v)
        indegree[v] += 1
    ancestors = [set() for _ in range(n)]

    queue = deque(i for i in range(n) if indegree[i] == 0)
    while queue:
        node = queue.popleft()
        for neighbor in adj[node]:
            ancestors[neighbor].add(node)
            ancestors[neighbor].update(ancestors[node])

            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                queue.append(neighbor)
    return [sorted(list(s)) for s in ancestors]


from collections import defaultdict


def countPairsOfConnectableServers(edges, signalSpeed):
    adj = defaultdict(list)

    # Build the adjacency list
    nodes = set()
    for u, v, w in edges:
        adj[u].append((v, w))
        adj[v].append((u, w))
        nodes.update([u, v])

    n = max(nodes) + 1
    result = [0] * n  # One result per node

    def dfs(node, parent, dist):
        nonlocal ct
        if dist % signalSpeed == 0:
            ct += 1
        for neighbor, weight in adj[node]:
            if neighbor != parent:
                dfs(neighbor, node, dist + weight)

    # For each node, find all valid pairs through it
    for root in range(n):
        temp = []
        for neighbor, weight in adj[root]:
            ct = 0
            dfs(neighbor, root, weight)
            temp.append(ct)

        # Count pairs from different branches
        total = 0
        prefix_sum = 0
        for ct in temp:
            total += prefix_sum * ct
            prefix_sum += ct
        result[root] = total

    return result


def minimumTime(n, edges, disappear):
    adj = defaultdict(list)
    for u, v, w in edges:
        adj[u].append((v, w))
        adj[v].append((u, w))

    minTime = [float("-inf")] * n
    visited = [False] * n

    heap = [(0, 0)]
    while heap:
        currTime, node = heapq.heappop(heap)
        if currTime >= disappear[node]:
            continue
        minTime[node] = currTime
        for neighbor, weight in adj[node]:
            nextTime = currTime + weight
            if nextTime < minTime[neighbor] and nextTime < disappear[neighbor]:
                minTime[neighbor] = nextTime
                heapq.heappush(heap, (nextTime, neighbor))
    return [t if t != float("inf") else -1 for t in minTime]


def findFarmland(land):
    m = len(land)
    n = len(land[0])
    result = [0]
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    def bfs(land,currI,currJ,row2,col2):
        queue=deque()
        queue.append((currI,currJ))
        while queue:
            i,j=queue.appendleft()
            row2=max(row2,currI)
            col2=max(col2,currJ)
            for d in dirs:
                _i=i+d[0]
                _j=j+d[1]
                if _i<len(land) and _i>=0 and _j<len(land[0]) and _j>=0 and land[currI+][currJ+i]==1:
                    queue.append((_i,_j))
                    land[_i][_j]=0


    def dfs(land, currI, currJ, row2, col2):
        land[currI][currJ] = 0
        row2 = max(currI, row2)
        col2 = max(currJ, col2)
        for d in dirs:
            i,j=d
            if currI+i<len(land) and currI+i>=0 and currJ+j<len(land[0]) and currJ+j>=0 and land[currI+][currJ+i]==1:
                land[currI+i][currJ+j]=0
                dfs(land,currI+i,currJ+j,row2,col2)

    for i in range(m):
        for j in range(n):
            if land[i][j] == 0:
                r1 = i
                c1 = j
                r2 = -1
                c2 = -1
                dfs(land, i, j, r2, c2)
                result.append({r1, c1, r2, c2})
    return result

def minReorder(n, connections):
    adj = defaultdict(list)
    for u, v, w in connections:
        adj[u].append((v, 1))
        adj[v].append((u, 0))
    result=0
    def dfs(adj,parent,curr):
        for node,checked in adj[curr]:
            if node !=parent:
                if checked==1:
                    result+=1
                dfs(adj,curr,node) 
    dfs(adj,-1,0)
    return result

def countPaths(n, roads):
    result = [float("inf")]*n
    count=[0]*n
    adj = defaultdict(list)
    m=pow(10,9)+7
    for u, v, w in roads:
        adj[u].append((v, w))
        adj[v].append((u, w))
    count[0]=1
    result[0]=0
    heap=[(0,0)]
    while heap:
        currTime,node=heapq.heappop(heap)
        for neig ,time in adj[node]:
            if currTime+time<result[neig]:
                result[neig]=currTime+time
                heapq.heappush(heap,(result[neig],neig))
                count[neig]=count[node]
            elif currTime+time==result[neig]:
                count[neig]=(count[node]+count[neig])%m
    return count





        