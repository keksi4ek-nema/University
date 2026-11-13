def recursyFib(n):
    if n == 1 or n == 2:
        return 1
    else:
        return recursyFib(n - 2) + recursyFib(n - 1)

def iterationFib(n):
    f1 = 1
    f2 = 1
    res = 1
    for i in range(3, n + 1):
        res = f1 + f2
        f1 = f2
        f2 = res
    return res

n = 5
print(f' n = {n} \n recursyFib(n) = {recursyFib(n)} \n iterationFib(n) = {iterationFib(n)}')
