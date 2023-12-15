def fib(n):
    a=[-1]*n
    a[0]=1
    a[1]=1
    for i in range(2,n):
        if a[i-1]==n:
            break
        else:
            a[i]=a[i-1]+a[i-2]
    return a

print(fib(7))