def mergeOverLappingIntervals(arr):
    arr.sort(key=lambda p: p[0])
    result = [[arr[0][0], arr[0][1]]]
    for i in range(1, len(arr)):
        startTime, endTime = result[-1]
        if endTime >= arr[i][0]:
            result[-1][1] = max(endTime, arr[i][1])
            result[-1][0] = min(startTime, arr[i][0])
        else:
            result.append([arr[i][0], arr[i][1]])
    return result


def insertInterval(arr, new):
    arr.sort(key=lambda p: p[0])
    for i in range(0, len(arr)):
        startTime, endTime = new
        if endTime >= arr[i][0]:
            arr[i][1] = max(endTime, arr[i][1])
            arr[i][0] = min(startTime, arr[i][0])
    newArr = mergeOverLappingIntervals(arr)
    return newArr


def intersectionOfTwoList(arr1, arr2):
    arr1.sort(key=lambda p: p[0])
    arr2.sort(key=lambda p: p[0])
    i = 0
    j = 0
    result = []
    while i < len(arr1) and j < len(arr2):
        startTime1 = arr1[i][0]
        startTime2 = arr2[j][0]
        endTime1 = arr1[i][1]
        endTime2 = arr2[j][1]
        if startTime1 <= endTime2 and startTime2 <= endTime1:
            result.append([max(startTime1, startTime2), min(endTime1, endTime2)])
        if endTime1 < endTime2:
            i += 1
        else:
            j += 1
    return result


import heapq


def minimumNumberOfMeeting(arr):
    # arr.sort(key=lambda p: p[0])
    # arr.sort(key=lambda p: p[0])
    # heap = []
    # heapq.heappush(heap, arr[0][1])
    # result = float("-inf")
    # for i in range(1, len(arr)):
    #     while heap and arr[i][0] >= 1 * heap[0]:
    #         heapq.heappop(heap)

    #     heapq.heappush(heap, arr[i][1])
    #     result = max(result, len(heap))
    # print(arr, result)
    endtime = []
    startime = []
    for i in range(len(arr)):
        endtime.append(arr[i][1])
        startime.append(arr[i][0])
    startime.sort()
    endtime.sort()
    i = 0
    j = 0
    count = 0
    result = 0
    while i < len(arr) and j < len(arr):
        if startime[i] > endtime[j]:
            count += 1
            i += 1
        elif endtime[j] >= startime[i]:
            count -= 1
            j += 1
        result = max(count, result)

    return result


def employeeFreeTime(arr):
    result = []
    for i in range(len(arr)):
        for j in range(len(arr[i])):
            result.append(arr[i][j])
    result.sort(key=lambda x: x[0])
    core = [result[0]]
    for i in range(1, len(result)):
        if core[-1][1] >= result[i][0]:
            core[-1][1] = max(core[-1][1], result[i][1])
            core[-1][0] = max(core[-1][0], result[i][0])
        else:
            core.append(result[i])
    return core


print(
    employeeFreeTime(
        [
            [[1, 2], [5, 6]],  # Employee A
            [[1, 3]],  # Employee B
            [[4, 10]],  # Employee C
        ]
    )
)
