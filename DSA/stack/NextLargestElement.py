def nextLargestElement(nums):
    result=[]
    stack=[]
    for i in range(len(nums)-1,-1,-1):
        if len(stack)==0:
            result.append(-1)
        elif len(stack)>0 and stack[-1]>nums[i]:
            result.append(stack[-1])
        elif len(stack)>0 and stack[-1]<=nums[i]:
            while len(stack)>0 and stack[-1]<=nums[i]:
                stack.pop()
            if len(stack)==0:
                result.append(-1)
            elif stack[-1]>nums[i]:
                result.append(stack[-1])
        stack.append(nums[i])
    # return result.reverse()
    result.reverse()
    print(result)
a=nextLargestElement([1,2,1])

def nextLargestElementToLeft(nums):
    result=[]
    stack=[]
    for i in range(len(nums)):
        if len(stack)==0:
            result.append(-1)
        elif len(stack)>0 and stack[-1]>nums[i]:
            result.append(stack[-1])
        elif len(stack)>0 and stack[-1]<=nums[i]:
            while len(stack)>0 and stack[-1]<=nums[i]:
                stack.pop()
            if len(stack)==0:
                result.append(-1)
            elif stack[-1]>nums[i]:
                result.append(stack[-1])
        stack.append(nums[i])
    print(result)
def nextSmallestToRightElement(nums):
    result=[]
    stack=[]
    for i in range(len(nums)-1,-1,-1):
        if len(stack)==0:
            result.append(-1)
        elif len(stack)>0 and stack[-1]<nums[i]:
            result.append(stack[-1])
        elif len(stack)>0 and stack[-1]>=nums[i]:
            while len(stack)>0 and stack[-1]>=nums[i]:
                stack.pop()
            if len(stack)==0:
                result.append(-1)
            elif stack[-1]<nums[i]:
                result.append(stack[-1])
        stack.append(nums[i])
    return result.reverse()
   
def nextSmallestLeftElement(nums):
    result=[]
    stack=[]
    for i in range(len(nums)):
        if len(stack)==0:
            result.append(-1)
        elif len(stack)>0 and stack[-1]<nums[i]:
            result.append(stack[-1])
        elif len(stack)>0 and stack[-1]>=nums[i]:
            while len(stack)>0 and stack[-1]>=nums[i]:
                stack.pop()
            if len(stack)==0:
                result.append(-1)
            elif stack[-1]<nums[i]:
                result.append(stack[-1])
        stack.append(nums[i])
    print(result)
def dailyTemperatures(temperatures):
        stack=[]
        result=[]
        for i in range(len(temperatures)-1,-1,-1):
            while len(stack)>0 and temperatures[i]>=temperatures[stack[-1]]:
                stack.pop()
            if len(stack)==0:
                result.append(0)
            else:
                result.append(stack[-1]-i)
            stack.append(i)
        return result[::-1]

        
print(dailyTemperatures([73,74,75,71,69,72,76,73]))
def removeDuplicates(s):
    stack=[]
    for i in range(len(s)):
        if len(stack)>0 and stack[-1]==s[i]:
            stack.pop()
        elif len(stack)==0 or stack[-1]!=s[i]:
            stack.append(s[i])
    ss=""
    for i in range(len(stack)):
            ss+=stack[i]
    return ss

print(removeDuplicates("abbaca"))

# def basicCalculator(s):
    
    
