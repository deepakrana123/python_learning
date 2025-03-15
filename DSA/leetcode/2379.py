from heapq import heapify, heappush, heappop

# def minimumRecolors(blocks, k):
#     dicts = {}
#     whiteColor = 0
#     blackColor = 0
#     i = 0
#     j = 0
#     minResult = float("inf")
#     while j < len(blocks):
#         whiteColor += 1 if blocks[j] == "W" else 0
#         blackColor += 1 if blocks[j] == "B" else 0
#         if whiteColor + blackColor == k:
#             minResult = min(whiteColor, minResult)
#             whiteColor -= 1 if blocks[i] == "W" else 0
#             blackColor -= 1 if blocks[i] == "B" else 0
#             i += 1
#         j += 1
#     return minResult


def closestPrimes(left, right):
    prime = [True for i in range(right + 1)]
    p = 2
    while p * p <= right:
        if prime[p] == True:
            for i in range(p * p, right + 1, p):
                prime[i] = False
        p += 1
    primes = []
    for i in range(left, right + 1):
        if prime[i]:
            primes.append(i)
    a = [-1, -1]
    minDiff = float("inf")
    for i in range(1, len(primes)):
        d = primes[i] - primes[i - 1]
        if d < minDiff:
            minDiff = d
            a[0] = primes[i - 1]
            a[1] = primes[i]
    return a


def findMaxSum(nums1, nums2, k):
    arr = []
    for i in range(len(nums1)):
        arr.append([nums1[i], i, nums2[i]])
    a = sorted(arr, key=lambda x: x[0])
    arra = [0] * len(nums1)
    heap = []
    heapify(heap)
    sums = 0
    for i in range(len(a)):
        if i > 0 and a[i - 1][0] == a[i][0]:
            ans = arra[a[i - 1][1]]
            arra[a[i][1]] = ans
        else:
            arra[a[i][1]] = sums
        heappush(heap, a[i][2])
        sums += a[i][2]
        while len(heap) > k:
            sums -= heappop(heap)
    return arra


def numberOfAlternatingGroups(colors, k):
    n = len(colors)
    result = 0
    length = 1
    last = colors[0]
    for i in range(1, n):
        if colors[i] == last:
            length = 1
            last = colors[i]
            continue
        length += 1
        if length >= k:
            result += 1
        last = colors[i]

    for i in range(k - 1):
        if colors[i] == last:
            length = 1
            last = colors[i]
            continue
        length += 1
        if length >= k:
            result += 1
        last = colors[i]
    return result


print(numberOfAlternatingGroups([0, 1, 0, 1, 0], k=3))
