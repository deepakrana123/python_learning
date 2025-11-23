def solve(self, text1, text2, i, j, dp):
    if i == len(text1) or j == len(text2):
        return 0
    if dp[i][j] != -1:
        return dp[i][j]
    if text1[i] == text2[j]:
        dp[i][j] = 1 + self.solve(text1, text2, i + 1, j + 1, dp)
        return dp[i][j]
    else:
        dp[i][j] = 1 + min(
            self.solve(text1, text2, i + 1, j, dp),
            self.solve(text1, text2, i, j + 1, dp),
        )
        return dp[i][j]


def shortestCommonSupersequence(str1: str, str2: str) -> str:
    dp = [[0 for _ in range(len(str2) + 1)] for _ in range(len(str1) + 1)]
    for i in range(len(str1) + 1):
        for j in range(len(str2) + 1):
            if i == 0 or j == 0:
                dp[i][j] = i + j
            elif str1[i - 1] == str2[j - 1]:
                dp[i][j] = 1 + dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1])
    result = []
    k = len(str1)
    l = len(str2)
    while k > 0 and l > 0:
        if str1[k - 1] == str2[l - 1]:
            result.append(str1[k - 1])
        else:
            if dp[k - 1][l] < dp[k][l - 1]:
                result.append(dp[k - 1])
            else:
                result.append(dp[k][l - 1])
    while k > 0:
        result.append(str1[k - 1])
        k -= 1
    while l > 0:
        result.append(str2[l - 1])
    return ",".join(result)


print(shortestCommonSupersequence("abac", "cab"))
