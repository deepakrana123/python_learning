# # a = [2, 1, 4, 3]
# # for i in range(0, len(a)):
# #     for j in range(i, len(a)):
# #         for k in range(j, len(a)):
# #             if a[i] < a[j] > a[k]:
# #                 # print(a[i],a[j],a[k])
# #                 break
# # # def iters(a):
# # #     if len(a)<3:
# # #         return 0
# # #     i=0
# # #     trip=[]
# # #     min_Element=float("inf")
# # #     max_Element=float("-inf")
# # #     for i in range(len(a)):
# # #         if a[i]<max_Element:
# # #             trip.append([min_Element,max_Element,a[i]])
# # #         else:
# # #             min_Element = min(min_Element,a[i])
# # #             max_Element = max(max_Element,a[i])
# # #     return trip


# # def fillbucket(s):
# #     count = 0
# #     cnt = 0
# #     isThree = False
# #     for ch in s:
# #         if ch == '.':
# #             cnt += 1
# #             count += 1
# #         else:
# #             cnt = 0
# #         if cnt == 3:
# #             isThree = True
# #             break
# #     if isThree:
# #         return 2
# #     else:
# #         return count


# # def minOperations(nums, k):
# #     result = 0
# #     for num in nums:
# #         result = result ^ num
# #     result = bin(result ^ k).replace("0b", "")
# #     count = 0
# #     for i in range(len(result)):
# #         if result[i] == '1':
# #             count += 1
# #     return count


# # def compress(s):
# #     c = 0
# #     for i in range(len(s)):
# #         if s[i] != '0':
# #             return s[i:]
# #     return 0


# # def compareVersion(version1, version2):
# #     a = version1.split('.')
# #     b = version2.split('.')
# #     if len(a) > len(b):
# #         c = len(a)-len(b)
# #         while c > 0:
# #             b.append('0')
# #             c -= 1
# #     elif len(a) < len(b):
# #         c = len(b)-len(a)
# #         while c > 0:
# #             a.append('0')
# #             c -= 1
# #     for i in range(len(a)):
# #         a[i] = compress(a[i])
# #         b[i] = compress(b[i])
# #     for i in range(len(a)):
# #         if int(a[i]) > int(b[i]):
# #             return 1
# #         elif int(a[i]) < int(b[i]):
# #             return -1
# #     return 0


# # def reversePrefix(word, ch):
# #     chIndex = 0
# #     for i in range(len(word)):
# #         if word[i] == ch:
# #             chIndex = i
# #             break
# #     a = word[0:chIndex+1]
# #     b = word[chIndex+1:]
# #     return a[::-1]+b


# # def addBinary(a, b):
# #     sums = ""
# #     curr = 0
# #     i = len(a)-1
# #     j = len(b)-1
# #     while (i >= 0 or j >= 0):
# #         if (int(a[i])+int(b[j]) == 2):
# #             sums += '0'
# #             curr = 1
# #         else:
# #             sums += str(int(a[i])+int(b[j]) + curr)

# #         # c=a[i]+ b[j] + curr
# #         # print(c,"hi")
# #         # sums+=c[1]
# #         # curr=c[0]
# #         # j-=1
# #         # i-=1
# #     print(sums, "sums")


# # print(addBinary("11", "1"))


# # def reverseLinkedList(head):
# #     if head is None or head.next is None:
# #         return head
# #     last = reverseLinkedList(head.next)
# #     head.next.next = head
# #     head.next = None
# #     return last


# # def removeNodes(head):
# #     stack = []
# #     maxs = float("-inf")
# #     curr = head
# #     while curr != None:
# #         stack.append(curr)
# #         curr = curr.next
# #     curr = stack[-1]
# #     stack.pop()
# #     maxs = max(curr.val, maxs)
# #     resultNode = curr


# # def doubleUtil(head):
# #     if head == None:
# #         return 0
# #     carryValue = doubleUtil(head.next)
# #     val = head.val*2 + carryValue
# #     head.val = val % 10
# #     return 1 if head.val >= 10 else 0


# # def doubleIt(head):
# #     # if head is None or head.next is None:
# #     #     return head
# #     # carryValue=doubleUtil(head)
# #     # if carryValue>0:
# #     #     newHead=ListNode(carry)
# #     #     carryValue.next=head
# #     #     return newHead
# #     # return head
# #     prev = None
# #     curr = head
# #     while curr != None:
# #         newVal = curr.val*2
# #         if newVal >= 10:
# #             curr.val = newVal % 10
# #             if prev != None:
# #                 prev.val += 1
# #             elif prev == None:
# #                 newHead = ListNode(1)
# #                 prev.next = curr
# #                 curr.val = newVal % 10
# #                 head = newHead
# #         else:
# #             curr.val = newVal
# #         prev = curr
# #         curr.next = curr
# #     return prev

# #     # head=reverseLinkedList(head)
# #     # curr=head
# #     # prev=None
# #     # carry=0
# #     # while(curr!=None):
# #     #     newValue=curr.val*2+carry
# #     #     curr.val=newValue%10
# #     #     if newValue>=10:
# #     #         carry=1
# #     #     else:
# #     #         carry=0
# #     # prev=curr
# #     # curr=curr.next
# #     # if carry !=0:
# #     #     newHead= ListNode(carry)
# #     #     prev.next=newHead
# #     # return reverseLinkedList(head)

# print("hello")


# def solve(nums, index, temp, result):
#     if index >= len(nums):
#         result.append(temp[:])
#         return
#     temp.append(nums[index])
#     solve(nums, index+1, temp, result)
#     temp.pop()
#     solve(nums, index+1, temp, result)


# def subset(nums):
#     result = []
#     solve(nums, 0, [], result)
#     return result


# print(subset([1, 2, 3]))


# def subsetXORSum(nums):
#     currSub = subset(nums)
#     result = 0
#     for edge in currSub:
#         xor = 0
#         for value in edge:
#             xor = xor ^ value
#         result += xor
#     return result
# # print(subsetXORSum([5,1,6]))


# # def matrixScore(grid):
# #     m = len(grid)
# #     n = len(grid[0])
# #     for i in range(m):
# #         if grid[i][0] == 0:
# #             for j in range(n):
# #                 grid[i][j] = 1-grid[i][j]
# #     for j in range(n):
# #         count_zero = 0
# #         for i in range(m):
# #             if grid[i][j] == 0:
# #                 count_zero += 1
# #         count_one = m-count_zero
# #         if count_zero > count_one:
# #             for i in range(n):
# #                 grid[i][j] = 1-grid[i][j]
# #     score = 0
# #     for i in range(m):
# #         for j in range(n):
# #             value = grid[i][j]*pow(2, n-j+i)
# #             score += value
# #     return score

# def specialArray(nums):
#     a = max(nums)
#     al = [0]*(a+1)

#     for value in nums:
#         al[value] += 1
#     for i in range(len(al)-2, -1, -1):
#         al[i] = al[i]+al[i+1]
#     for i in range(len(al)):
#         if i == al[i]:
#             return i


# print(specialArray([0, 4, 3, 0, 4]))


# def equalSubstring(s, t, maxCost):
#     i = 0
#     j = 0
#     n = len(s)
#     maxResult = 0
#     cost = 0
#     while (i < n and j < n):
#         while cost > maxCost:
#             maxResult = max(maxResult, j-i+1)
#             i += 1
#         cost = cost+ord(s[i])-ord(t[i])
#         j += 1
#     return maxResult


# def isBananaEmpty(piles, mid, h):
#     actualHours = 0
#     for value in piles:
#         actualHours += value//mid
#         if value % h != 0:
#             actualHours += 1
#     return actualHours <= h


# def minEatingSpeed(piles, h):
#     right = max(piles)
#     start = 1
#     while start < right:
#         mid = (right+start)//2
#         if isBananaEmpty(piles, mid, h):
#             right = mid
#         else:
#             start = mid+1
#     return start


# print(minEatingSpeed([3, 6, 7, 11], 8), "hi")


# def totalTrip(time, mid, totalTrips):
#     trip=0
#     for value in time:
#         trip+=mid//value
#     return trip==totalTrips

# def minimumTime(time, totalTrips):
#     right = max(time)
#     start = 1
#     while start < right:
#         mid = (right+start)//2
#         if totalTrip(time, mid, totalTrips):
#             right = mid
#         else:
#             start = mid+1
#     return start
# print(minimumTime([1,2,3],5),"hihhihii")

# import math
# def successfulPairs(spells, potions, success):
#     potions.sort()

# print(successfulPairs( [5,1,3], [1,2,3,4,5],7))


# def numberOfSubarrays(nums, k):
#     oddCountMap = {}
#     oddCount = 0
#     oddCountMap[oddCount] = 1
#     result = 0
#     for i in range(len(nums)):
#         oddCount += (nums[i] % 2)
#         if oddCount-k in oddCountMap:
#             result += oddCountMap[oddCount-k]
#         oddCountMap[oddCount] = oddCountMap.get(oddCount,0)+1
#     return result
# print(numberOfSubarrays([2, 2, 2, 1, 2, 2, 1, 2, 2, 2],  2))

# def wordMake(dicts,words):
#     r=""
#     for i in range(len(words)):
#         r=words[0:i]
#         if r in dicts:
#             return r
#     return words
# def replaceWords(dictionary, sentence):
#     a=sentence.split(" ")
#     result=""
#     for i in range(len(a)):
#         result = result+wordMake(dictionary,a[i]) + " "
#     return result.strip()
# print(replaceWords(["cat","bat","rat"], "the cattle was rattled by the battery"
# ))

# def isNStraightHand( hand, groupSize):
#         n=len(hand)
#         if n % groupSize!=0:
#             return False
#         dicts={}
#         for value in hand:
#             if value in dicts:
#                 dicts[value]+=1
#             else:
#                 dicts[value]=1
#         while dicts:
#             first_key = next(iter(dicts))
#             for i in range(groupSize):
#                 if dicts[first_key+i] ==0:
#                     return False
#                 dicts[first_key+i]-=1
#                 if dicts[first_key+i]<1:
#                     del dicts[first_key+i]
#         return True
# print(isNStraightHand( [1,2,3,6,2,3,4,7,8],3))       
def minKBitFlips(nums, k):
    
         
        