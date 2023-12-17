# def isPredecessor(s, t):
#     i = 0
#     j = 0
#     m = len(s)
#     n = len(t)
#     if m >= n or n - m != 1:
#         return False
#     while i < m and j < n:
#         if s[i] == t[j]:
#             i = i + 1
#         j = j + 1
#     return i == m
# def solve(sortbylength, index, previous, dp):
#     if index == len(sortbylength):
#         return 0
#     if dp[index][previous + 1] != -1:
#         return dp[index][previous + 1]
#     take = 0
#     if previous == -1 or isPredecessor(sortbylength[previous], sortbylength[index]):
#         take = 1 + solve(sortbylength, index + 1, index, dp)
#     not_take = solve(sortbylength, index + 1, previous, dp)
#     dp[index][previous + 1] = max(not_take, take)
#     return dp[index][previous + 1]
# def longestStrChain(words):
#     sortbylength = sorted(words, key=len)
#     dp = [[-1 for i in range(len(words)+1)] for _ in range(len(words))]
#     return solve(sortbylength, 0, -1, dp)
# print(longestStrChain(["xbc", "pcxbcf", "xb", "cxbc", "pcxbc"]))
def isPredecessor(s, t):
    # Function to check if s is a predecessor of t
    if len(t) - len(s) != 1:
        return False

    i = 0
    j = 0
    while i < len(s) and j < len(t):
        if s[i] == t[j]:
            i += 1
        j += 1

    return i == len(s)

def solve(sortbylength, index, previous, dp):
    # Dynamic programming function to find the length of the longest string chain
    if index == len(sortbylength):
        return 0
    
    if dp[index][previous + 1] != -1:
        return dp[index][previous + 1]

    take = 0
    if previous == -1 or isPredecessor(sortbylength[previous], sortbylength[index]):
        take = 1 + solve(sortbylength, index + 1, index, dp)
    
    not_take = solve(sortbylength, index + 1, previous, dp)
    
    dp[index][previous + 1] = max(not_take, take)
    return dp[index][previous + 1]

def longestStrChain(words):
    # Main function to find the length of the longest string chain
    sortbylength = sorted(words, key=len)
    dp = [[-1 for _ in range(len(words) + 1)] for _ in range(len(words))]
    return solve(sortbylength, 0, -1, dp)

# Test case
print(longestStrChain(["xbc", "pcxbcf", "xb", "cxbc", "pcxbc"]))

# by bottom up
def longestStrChain(self, nums) -> int:
        sortbylength=sorted(nums,key=len)
        # dp=[[-1 for i in range(len(words)+1)] for j in range(len(words))]
        # return self.solve(sortbylength,0,-1,dp)
        dp=[1 for i in range(len(nums))]
        max1=1
        for i in range(len(sortbylength)):
            for j in range(i):
                if self.isPredecessor(sortbylength[j],sortbylength[i]):
                    dp[i]=max(dp[i],dp[j]+1)
                    max1=max(max1,dp[i])
        return max1 

