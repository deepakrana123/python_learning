def minRemoveToMakeValid(s):
    stack=[]
    removeId=set()
    for i in range(len(s)):
        if s[i]=='(':
            stack.append(i)
        elif s[i]==')':
            if stack:
                stack.pop()
            else:
                removeId.add(i)
    while stack:
        removeId.add(stack[-1])
        stack.pop()
    result=""
    for i in range(len(s)):
        if i in removeId:
            continue
        else:
            result+=s[i]
    return result
print(minRemoveToMakeValid("a)b(c)d"))
        