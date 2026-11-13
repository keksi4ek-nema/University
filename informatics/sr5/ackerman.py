def ackerman(m, n):
    if m == 0:
        return n + 1
    elif n == 0:
        return ackerman(m - 1, 1)
    else:
        return ackerman(m - 1, ackerman(m, n - 1))

m, n = 1, 2
print(f' m = {m}, n = {n} \n ackerman(m, n) = {ackerman(m, n)}')
