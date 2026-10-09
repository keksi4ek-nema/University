#2.7 Факторизация числа



#
#Рекурсивная факторизация методом пробного деления
#
def factor_recursive(n, d=2):
    if n < 2:
        return []

    if d * d > n:
        return [n]

    if n % d == 0:
        return [d] + factor_recursive(n // d, d)

    return factor_recursive(n, d + 1)



#
#Итеративная факторизация методом пробного деления
#


def factor_iter(n):
    if n < 2:
        return []

    result = []
    d = 2

    while d * d <= n:
        while n % d == 0:
            result.append(d)
            n = n // d

        d += 1

    if n > 1:
        result.append(n)

    return result


#
#Факторизация с помощью таблицы SPF
#



def build_spf(N):
    spf = list(range(N + 1))

    if N >= 1:
        spf[1] = 1

    for i in range(2, int(N ** 0.5) + 1):
        if spf[i] == i:  # i — простое число
            for j in range(i * i, N + 1, i):
                if spf[j] == j:
                    spf[j] = i

    return spf


def factor_spf(n, spf):
    if n < 2 or n >= len(spf):
        return []

    result = []

    while n > 1:
        p = spf[n]
        result.append(p)
        n = n // p

    return result

#
#Проверка работы функций факторизации
#



spf = build_spf(100)
factorization_number = 60







print(f"Факторизация числа {factorization_number} (итеративно): {factor_iter(factorization_number)}")

print(f"Факторизация числа {factorization_number} (рекурсивно): {factor_recursive(factorization_number)}")

print(f"Факторизация числа {factorization_number} (через SPF): {factor_spf(factorization_number, spf)}")

print(f"Факторизация числа 84 (через SPF): {factor_spf(84, spf)}")