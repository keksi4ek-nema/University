def macarty(n):
    if n > 100:
        return n - 10
    else:
        return macarty(macarty(n + 11))


spisok = [80, 91, 99, 100, 101, 105, 110]
for n in spisok:
    print(f"macarty({n}) = {macarty(n)}")
