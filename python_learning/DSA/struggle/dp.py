class Solution:
    def knapSack(self, val, wt, capacity):
        n = len(val)
        dp = {}

        def solve(start, capacity):
            if start == 0:
                return (capacity // wt[0]) * val[0]
            if (start, capacity) in dp:
                return dp[(start, capacity)]
            skip = solve(start - 1, capacity)
            taken = 0
            if capacity - wt[start] >= 0:
                taken = val[start] + solve(start, capacity - wt[start])
            dp[(start, capacity)] = max(taken, skip)
            return dp[(start, capacity)]

        return solve(n - 1, capacity)

    def cutRod(self, price):
        n = len(price)
        dp = {}

        def solve(index, capacity):
            if index == 0:
                return (capacity // 1) * price[0]
            if (index, capacity) in dp:
                return dp[(index, capacity)]
            skip = solve(index - 1, capacity)
            taken = 0
            rod_len = index + 1
            if capacity >= rod_len:
                taken = price[index] + solve(index, capacity - rod_len)
            dp[(index, capacity)] = max(taken, skip)
            return dp[(index, capacity)]

        return solve(n - 1, n)

    def coinChange(coins, amount):
        n = len(coins)
        dp = {}

        def solve(index, capacity):
            if index >= len(coins):
                if capacity == 0:
                    return 0
                return float("inf")
            if (index, capacity) in dp:
                return dp[(index, capacity)]
            skip = solve(index + 1, capacity)
            taken = float("inf")
            if capacity >= coins[index]:
                taken = 1 + solve(index, capacity - coins)
            dp[(index, capacity)] = min(taken, skip)
            return dp[(index, capacity)]

        return solve(0, amount)

    def partition(self, s: str):
        result = []
        temp = []
        dp = {}
        dp_partiton = [[0 for _ in range(len(s))] for _ in range(len(s))]

        for L in range(1, len(s) + 1):
            for i in range(len(s) - L + 1):
                j = i + L - 1
                if i == j:
                    dp_partiton[i][j] = 1
                if s[i] == s[j]:
                    if L == 2:
                        dp_partiton[i][j] = 1
                    else:
                        dp_partiton[i][j] = dp_partiton[i + 1][j - 1]

        def isPalindrome(start, end, s):
            if start > end:
                return True
            if s[start] != s[end]:
                return False
            if s[start] == s[end]:
                return isPalindrome(start + 1, end - 1, s)

        def solve(start):
            if start >= len(s):
                result.append(temp[:])
                return
            if start in dp:
                return dp[start]
            for j in range(start, len(s)):
                if isPalindrome(start, j, s):
                    temp.append(s[start : j + 1])
                    solve(j + 1)
                    temp.pop()

        return solve(0)

    def subarraySum(nums, k):
        def solve(index, target):
            if target == k:
                return True
            if index == 0 and nums[0] == target:
                return True

            return solve(index, target) or solve(index - 1, target - nums[index])

        dp = [[False for _ in range(k + 1)] for _ in range(len(nums))]
        for i in range(len(nums) + 1):
            dp[i][0] = True
        dp[0][nums[0]] = True

        for i in range(1, len(nums)):
            for j in range(1, k + 1):
                dp[i][j] = dp[i - 1][j] or dp[i - 1][k - nums[i]]
        return dp[len(nums) - 1][k]

        # return solve(len(nums) - 1, k)
        # count = 0
        # prefix = 0
        # freq = {0: 1}
        # for num in nums:
        #     prefix += num
        #     count += freq.get(prefix - k, 0)
        #     freq[prefix] = freq.get(prefix, 0) + 1
        # return count

    def canPartiton(arr, k):
        totalSums = sum(arr)
        # dp = {}
        if sum(arr) % 2 != 0:
            return False

        # def solve(index, target):
        #     if target == 0:
        #         return True
        #     if (index, target) in dp:
        #         return dp[(index, target)]
        #     if index == 0 and arr[0] == target:
        #         return True
        #     dp[(index, target)] = solve(index, target) or solve(
        #         index - 1, target - arr[index]
        #     )
        #     return dp[(index, target)]

        # return solve(len(arr) - 1, totalSums - k)
        dp = [[False for _ in range(totalSums - k + 1)] for _ in range(len(arr))]
        for i in range(len(arr) + 1):
            dp[i][0] = True
        dp[0][arr[0]] = True

        for i in range(1, len(arr)):
            for j in range(1, totalSums - k + 1):
                dp[i][j] = dp[i - 1][j] or dp[i - 1][j - arr[i]]
        return dp[len(arr) - 1][totalSums - k]

    def minimumDifference(nums):
        totalSums = sum(nums)
        dp = [[False for _ in range(totalSums)] for _ in range(len(nums))]
        for i in range(len(nums)):
            dp[i][0] = True
        if nums[0] <= totalSums:
            dp[0][nums[0]] = True

        for i in range(1, len(nums)):
            for j in range(1, totalSums + 1):
                notTake = dp[i - 1][j]
                take = False
                if nums[i] <= j:
                    take = dp[i - 1][j - nums[i]]
                dp[i][j] = notTake or take

        minValue = float("inf")
        for i in range(totalSums // 2 + 1):
            if dp[len(nums) - 1][i] == True:
                minValue = min(minValue, abs(totalSums - i) - i)
        return minValue


from typing import List
import bisect


class Solution:
    def minimumDifference(self, nums: List[int]) -> int:
        n = len(nums) // 2
        totalSum = sum(nums)

        def getSubsetSums(arr):
            res = [[] for _ in range(len(arr) + 1)]

            def backtrack(index, curr_sum, count):
                if index == len(arr):
                    res[count].append(curr_sum)
                    return
                # Take current
                backtrack(index + 1, curr_sum + arr[index], count + 1)
                # Don't take
                backtrack(index + 1, curr_sum, count)

            backtrack(0, 0, 0)
            return res

        left = nums[:n]
        right = nums[n:]

        leftSums = getSubsetSums(left)  # All subset sums of left half, grouped by size
        rightSums = getSubsetSums(
            right
        )  # All subset sums of right half, grouped by size

        minDiff = float("inf")

        for l in range(n + 1):
            leftGroup = leftSums[l]
            rightGroup = rightSums[n - l]
            rightGroup.sort()

            for leftSum in leftGroup:
                target = totalSum // 2 - leftSum
                idx = bisect.bisect_left(rightGroup, target)

                # check rightGroup[idx]
                if idx < len(rightGroup):
                    currSum = leftSum + rightGroup[idx]
                    minDiff = min(minDiff, abs((totalSum - currSum) - currSum))

                # check rightGroup[idx - 1]
                if idx > 0:
                    currSum = leftSum + rightGroup[idx - 1]
                    minDiff = min(minDiff, abs((totalSum - currSum) - currSum))

        return minDiff
