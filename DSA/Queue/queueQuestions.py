from collections import deque
def modifyQueue(s,k):
    q = deque()
    st=[]
    for n in s:
        q.append(n)
    n=len(q)
    remaining=n-k
    reversed(st)
    while(k>0):
        st.append(q.popleft)
        q.pop()
        k=k-1
    while st:
        q.append(st[-1])
        st.pop()
    while remaining:
        q.append(q.popleft())
        q.pop()
    return q
        