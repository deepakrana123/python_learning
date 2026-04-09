def countOfSubstrings(word, k):
    constIndex = [0] * len(word)
    constFound = len(word)
    for i in range(len(word) - 1, -1, -1):
        if word[i] not in "aeiou":
            constIndex[i] = constFound
            constFound = i
        else:
            constIndex[i] = constFound
    i = 0
    j = 0
    dicts = {}
    constCount = 0
    count = 0
    while j < len(word):
        if word[j] in "aeiou":
            dicts[word[j]] = dicts.get(word[j], 0) + 1
        else:
            constCount += 1
        while i < len(word) and constCount > k:
            ch = word[i]
            if ch in "aeiou":
                dicts[ch] -= 1
                if dicts[ch] == 0:
                    del dicts[ch]
            else:
                constCount -= 1
            i += 1

        while i < len(word) and len(dicts) == 5 and constCount == k:
            idx = constIndex[j]
            count += idx - j
            ch = word[j]
            if ch in "aeiou":
                dicts[ch] -= 1
                if dicts[ch] == 0:
                    del dicts[ch]
            else:
                constCount -= 1
            i += 1
        j += 1
    return count


# print(countOfSubstrings("ieaouqqieaouqq", k=1))


# def repairCars(ranks, cars):
# def countDays(days, meetings):
#     meetings.sort(key=lambda item: item[0])
#     start = 0
#     end = 0
#     count = 0
#     for i in range(1, len(meetings)):
#         if meetings[i][0] >= end:
#             count += meetings[i][0] - end - 1
#         end = max(meetings[i][1], end)
#     if days > end:
#         count += days - end
#     return count


# def countPaths(n, roads):
#     graph = {i: [] for i in range(n + 1)}
#     result = [float("inf")] * (n + 1)
#     pathCount = [0] * (n + 1)
#     pathCount[0] = 1
#     priority_queue = [(0, 0)]
#     while priority_queue:
#         currTime, currNode = priority_queue.pop()
#         for vec in graph[currNode]:
#             ngbr = vec[0]
#             roadTime = vec[1]
#             if currTime + roadTime < result[ngbr]:
#                 result[ngbr] = currTime + roadTime
#                 priority_queue.append((result[ngbr], ngbr))
#                 pathCount[ngbr] = pathCount[currNode]
#             elif currTime + roadTime == result[ngbr]:
#                 pathCount[ngbr] = pathCount[ngbr] + pathCount[currNode]
#     return pathCount[len(roads) - 1]


# print(
#     countPaths(
#         n=7,
#         roads=[
#             [0, 6, 7],
#             [0, 1, 2],
#             [1, 2, 3],
#             [1, 3, 3],
#             [6, 3, 3],
#             [3, 5, 1],
#             [6, 5, 1],
#             [2, 5, 1],
#             [0, 4, 5],
#             [4, 6, 2],
#         ],
#     )
# )


def checkValidCuts(n, rectangles):
    x = []
    y = []
    for startx, starty, endx, endy in rectangles:
        x.append([startx, endx])
        y.append([starty, endy])
    x.sort(key=lambda item: item[0])
    y.sort(key=lambda item: item[0])
    resultx = [x[0]]
    resulty = [y[0]]
    for i in range(1, len(x)):
        if x[i][0] < resultx[-1][1]:
            resultx[-1][1] = max(x[i][1], resultx[-1][1])
        else:
            resultx.append(x[i])
    for i in range(1, len(y)):
        if y[i][0] < resulty[-1][1]:
            resulty[-1][1] = max(y[i][1], resulty[-1][1])
        else:
            resulty.append(y[i])
    if len(resultx) >= 3:
        return True
    elif len(resulty) >= 3:
        return True
    return False


print(
    checkValidCuts(
        4,
        rectangles=[
            [0, 2, 2, 4],
            [1, 0, 3, 2],
            [2, 2, 3, 4],
            [3, 0, 4, 2],
            [3, 2, 4, 4],
        ],
    )
)
