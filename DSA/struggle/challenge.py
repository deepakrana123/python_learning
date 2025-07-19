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
