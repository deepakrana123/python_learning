def relativeSortArray(arr1, arr2):
    dict1 = {}
    for value in arr1:
        if value in dict1:
            dict1[value] += 1
        else:
            dict1[value] = 1

    v = []
    for value in arr2:
        for i in range(dict1[value]):
            v.append(value)
            dict1[value] -= 1
        if dict1[value] == 0:
            del dict1[value]

    for value in dict1:
        v.append(value)
    return v

# import math
# def judgeSquareSum(c):
#     value=math.sqrt(c)
#     a=[]
#     dict1={}
#     for i in range(int(value)+1):
#         a.append(i)
#     for i in range(len(a)):
#         print(a[i])
#         sums=c-a[i]*a[i]
#         if math.sqrt(sums) in dict1:


#     print(value,a)
# print(judgeSquareSum(5))

# def dfs(ancestor,adj,currNode,result):

#     for value in adj[currNode]:
#         if result[value] or ancestor not in result[value]:
#             result[value].add(ancestor)
#             dfs(ancestor,adj,value,result)

# def getAncestors(n, edges):
#     result = [set() for _ in range(n)]
#     dict1={}
#     for value in edges:
#         u,v=value
#         dict1[u].append(v)
#     for i in range(n):
#         ancestor=i
#         dfs(ancestor,dict1,i,result)
#     return result


def sumOddLengthSubarrays(arr):
    print(len(arr))
    subs = []
    for i in range(1, len(arr)+1, 2):
        for j in range(len(arr)-i+1):
            subs.append(arr[j:j+i])
    sums = 0
    for value in subs:
        sums += sum(value)
    return sums


print(sumOddLengthSubarrays([1, 4, 2, 5, 3]))


def longestAlternatingSubarray(nums, threshold):
    l = 0
    for i in range(len(nums)):
        if nums[i] % 2 == 0:
            l = 0
            break
    count = 0
    for i in range(l+1, len(nums)):
        if nums[i-1] % 2 != nums[i] % 2 and nums[i-1] <= threshold and nums[i] <= threshold:
            count += 1
    print(count, "count")
# print(longestAlternatingSubarray([2,3,4,5],4))


def minDifference(nums):
    a = sorted(nums)
    m = len(a)
    n = a[len(a)-1-3]
    for i in range(m-3, m):
        a[i] = n
    return max(a)-min(a)
# print(minDifference([3,100,20]))


def buildTree(left, right, tree, index, root):
    if left == right:
        tree[index] = root[left]
        return tree[index]
    mid = left+(right-left)//2
    buildTree(left, mid, tree, 2*index+1, root)
    buildTree(mid+1, right, tree, 2*index+2, root)
    tree[index] = tree[2*index+1] + tree[2*index+2]
    return tree[index]


# def rangeSumBST(root):
#     segementTree = [0]*len(root)*4
#     buildTree(0, len(root)-1, segementTree, 0, root)
#     return segementTree
# print(rangeSumBST([10,5,15,3,7,None,18]))

def nodesBetweenCriticalPoints(head):