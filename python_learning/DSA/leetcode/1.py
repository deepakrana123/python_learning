# class Solution:
#     def count2Frequency(self,dicts):
#         for key,value in dicts.items():
#             if dicts[key]==2:
#                 return True
#         return False

#     def lengthOfLongestSubstring(self, s: str) -> int:
#         i=0
#         j=0
#         ans=float("-inf")
#         n=len(s)
#         dicts={}
#         while j<n:
#             dicts[s[j]]=dicts.get(s[j],0)+1
#             if self.count2Frequency(dicts):
#                 while self.count2Frequency(dicts):
#                     dicts[s[i]]-=1
#                     if dicts[s[i]]==0:
#                         del dicts[s[i]]
#                     i+=1
#             ans=max(ans,j-i+1)
#             j+=1
#         return ans
# a=Solution()
# print(a.lengthOfLongestSubstring("abcabcbb"))
# class Solution:
#     def count2Frequency(self,dicts):
#         for key,value in dicts.items():
#             if dicts[key]==2:
#                 return True
#         return False

#     def maximumUniqueSubarray(self, s) -> int:
#         if len(s)==0:
#             return 0
#         ans=float("-inf")
#         i=0
#         j=0
#         n=len(s)
#         dicts={}
#         sums=0
#         while j<n:
#             if s[j] in dicts:
#                 while s[j] in dicts:
#                     sums -= s[i]
#                     dicts[s[i]] -= 1
#                     if dicts[s[i]] == 0:
#                         del dicts[s[i]]
#                     i += 1
#             dicts[s[j]]=dicts.get(s[j],0)+1
#             sums+=s[j]
#             ans=max(ans,sums)
#             j+=1
#         return ans
# a=Solution()
# print(a.maximumUniqueSubarray([4,2,4,5,6]))


# class Solution:
#     def check_vowel_order(self, char1, char2):
#         vowels = "aeiou"
#         index1 = vowels.find(char1)
#         index2 = vowels.find(char2)
#         if index1 != -1 and index2 == index1 + 1:
#             return True
#         else:
#             return False

#     def longestBeautifulSubstring(self, word: str) -> int:
#         if len(word) < 5:
#             return 0
#         l = 0
#         r = 0
#         for i in range(len(word)):
#             if word[i] == "a":
#                 l = i
#                 r = i
#                 break
#         prev = r
#         r = r + 1
#         maxLength = 0
#         while r < len(word):
#             if self.check_vowel_order(word[prev], word[r]):
#                 maxLength = max(maxLength, r - l + 1)
#             while self.check_vowel_order(word[prev], word[r]) == False:
#                 prev = l
#                 l += 1
#             prev = r
#             r += 1

#         return maxLength


# def minimumIndex(arr):
#     candidate = -1
#     votes = 0
#     n = len(arr)
#     for i in range(n):
#         if votes == 0:
#             candidate = arr[i]
#             votes = 1
#         else:
#             if arr[i] == candidate:
#                 votes += 1
#             else:
#                 votes -= 1
#     majorityCount = 0
#     for num in arr:
#         if num == candidate:
#             majorityCount += 1

#     count = 0
#     for i in range(n):
#         if arr[i] == candidate:
#             count += 1
#         n1 = i + 1
#         n2 = n - i - 1
#         remainingcount = majorityCount - count
#         if count * 2 > n1 and remainingcount * 2 > n2:
#             return i
#     return -1


# print(minimumIndex([1, 2, 2, 2]))
def partitionLabels(s):
    dicts = {}
    for i in range(len(s)):
        if s[i] in dicts:
            dicts[s[i]] = max(dicts[s[i]], i)
        dicts[s[i]] = i
    start = 0
    end = 0
    result = []
    while start < len(s):
        end = dicts[s[start]]
        j = start
        while j < end:
            end = max(dicts[s[j]], end)
            j += 1
        result.append(j - start + 1)
        start = j + 1

    return result


import heapq


def maxPoints(grid, queries):
    sorted = []
    result = [0] * len(queries)
    for i in range(len(queries)):
        sorted.append((queries[i], i))
    sorted.sort(key=lambda item: item[0])
    visited = [[False for _ in range(len(grid[0]))] for _ in range(len(grid))]
    points = 0
    priority_queue = [(grid[0][0], 0, 0)]
    heapq.heapify(priority_queue)
    visited[0][0] = True
    directions = [(-1, 0), (0, -1), (1, 0), (0, 1)]
    for x in range(len(sorted)):
        query = sorted[x][0]
        index = sorted[x][1]
        while priority_queue and priority_queue[0][0] < query:
            value, i, j = heapq.heappop(priority_queue)
            points += 1
            for dir in directions:
                new_x = i + dir[0]
                new_y = j + dir[1]
                if (
                    new_x >= 0
                    and new_y >= 0
                    and new_y < len(grid[0])
                    and new_x < len(grid)
                    and visited[new_x][new_y] == False
                ):
                    heapq.heappush(priority_queue, (grid[new_x][new_y], new_x, new_y))
                    visited[new_x][new_y] = True
        result[index] = points
    return result


def minOperations(grid, x):
    sorted = []
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            sorted.append(grid[i][j])
    sorted.sort()
    target = sorted[len(sorted) // 2]
    result = 0
    for num in sorted:
        if num % x != target % x:
            return -1
        result += abs(target - num) // x
    return result
