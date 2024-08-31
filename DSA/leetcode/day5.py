from collections import deque 
def countStudents(students, sandwiches):
        a=[0]*2
        for key in students:
            a[key]+=1
        d=0
        for i in range(len(sandwiches)):
            if a[sandwiches[i]]==0:
                return len(sandwiches)-i
            a[sandwiches[i]]-=1
        return 0
def countStud(students, sandwiches):
    queue=deque(students)
    
        