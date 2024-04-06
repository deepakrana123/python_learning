def productExceptSelf(nums):
    left = [1]
    right = [0]*(len(nums))
    right[len(nums)-1] = 1
    for i in range(1, len(nums)):
        left.append(nums[i-1]*left[i-1])
    for i in range(len(nums)-2, -1, -1):
        right[i] = nums[i+1]*right[i+1]
    result = [0]*len(nums)
    for i in range(len(nums)):
        result[i] = left[i]*right[i]
    return result


def subarraySum(nums, k):
    left = [0]*len(nums)
    left[0] = nums[0]
    for i in range(1, len(nums)):
        left[i] = nums[i]+left[i-1]
    dict1 = {}
    dict1[0] = 1
    result = 0
    for i in range(len(left)):
        val = left[i]-k
        if val in dict1:
            result += dict1[val]
            dict1[val] += 1
        else:
            dict1[left[i]] = 1
    return result


def binarySubarraySum(num, goal):
    window_sum = 0
    i = 0
    j = 0
    counts = 0
    count_zeros = 0
    while (j < len(num)):
        window_sum += num[j]
        while (i < len(num) and (num[i] == 0 or window_sum > goal)):
            if (num[i] == 0):
                count_zeros += 1
            else:
                count_zeros = 0
            window_sum -= num[i]
            i += 1
        if window_sum == goal:
            counts = 1+count_zeros
        j += 1
    return counts
def countSubstrings(s, c):
    dict1=0
    result=0
    for string in s:
        if string==c:
            result=1+dict1+result
            dict1+=1
    return result
        
def insert(intervals, newInterval):
        i=0
        n=len(intervals)
        result=[]
        while(i<n):
            if intervals[i][1]<newInterval[0]:
                result.append(intervals[i])
            elif intervals[i][0]>newInterval[1]:
                break
            else:
                newInterval[0]=min(newInterval[0],intervals[i][0])
                newInterval[1]=max(newInterval[1],intervals[i][1])
            i+=1
        result.append(newInterval)
        while(i<n):
            result.append(intervals[i])
            i+=1
        return result    
print(insert( [[1,3],[6,9]],[2,5]))