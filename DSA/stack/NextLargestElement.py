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
