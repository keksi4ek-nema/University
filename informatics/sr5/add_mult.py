def Z(x):
    return 0

def I(x):
    return x

def Inc(x):
    return x + 1

def recursyAdd(x, y):
    if y == 0:
        return I(x)
    else:
        return Inc(recursyAdd(x, y - 1))

def iterationAdd(x, y):
    res = I(x)
    i = Z(y)
    while i < y:
        res = Inc(res)
        i = Inc(i)
    return res

def recursyMult(x, y):
    if y == 0:
        return Z(x)
    else:
        return recursyAdd(recursyMult(x, y - 1), x)

def iterationMult(x, y):
    res = Z(x)
    i = Z(y)
    while i < y:
        res = iterationAdd(res, x)
        i = Inc(i)
    return res

x, y = 4, 2
print(f' x = {x}, y = {y} \n recursyAdd(x, y) = {recursyAdd(x, y)} \n iterationAdd(x, y) = {iterationAdd(x, y)} \n recursyMult(x, y) = {recursyMult(x, y)} \n iterationMult(x, y) = {iterationMult(x, y)}')

