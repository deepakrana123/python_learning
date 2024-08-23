
def solve(satisfaction, index, time, dp):
        if index >= len(satisfaction):
            return 0
        if dp[index][time] != -1:
            return dp[index][time]
        taken = satisfaction[index]*time + \
            self.solve(satisfaction, index+1, time+1, dp)
        skip = self.solve(satisfaction, index+1, time, dp)
        dp[index][time] = max(taken, skip)
        return dp[index][time]

def maxSatisfaction(satisfaction):
        # satisfaction.sort()
        # # return self.solve(satisfaction,0,1,dp)
        satisfaction.sort()
        n = len(satisfaction)
    # DP table initialization
        dp = [[0] * (n + 1) for _ in range(n + 1)]

        for i in range(1, n + 1):
            for time in range(1, i + 1):
                dp[i][time] = max(
                    dp[i-1][time], satisfaction[i-1] * time + dp[i-1][time-1])

        return max(dp[n])
