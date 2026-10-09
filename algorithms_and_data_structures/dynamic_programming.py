#2.5 Динамическое програмирование
#
#Вычисление числа Фибоначчи разными способами 
#
#Простая рекурсия
#
def fib_naive(n: int) -> int:
    if n <= 1:
        return n
    return fib_naive(n - 1) + fib_naive(n - 2)

#
#Мемоизация, сохранение уже вычисленных значений, для переиспользования
#


def fib_memo(n: int, memo: list | None = None) -> int:
    if memo is None:
        memo = [-1] * (n + 1)

    if n <= 1:
        return n
    if memo[n] != -1:
        return memo[n]

    memo[n] = fib_memo(n - 1, memo) + fib_memo(n - 2, memo)
    return memo[n]


#
#Табуляция, построение решения снизу вверх
#

def fib_tab(n: int) -> int:
    if n <= 1:
        return n

    dp = [0] * (n + 1)
    dp[0], dp[1] = 0, 1

    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]

    return dp[n]


print("Вычисление числа Фибоначчи тремя разными способами:")
for n in [0, 1, 5, 10]:
    print(f"n={n}: простая рекурсия={fib_naive(n)}, Мемоизация={fib_memo(n)}, Табуляция={fib_tab(n)}")
    