from recursion import output_letter
from tower_of_hanoi import hanoi_iterative, hanoi_tower
from recursive_to_non_recursive import sum_range, sum_range_iter, sum_range_stack
from recursion_a_search_method import search
from dynamic_programming import fib_memo, fib_naive, fib_tab
from knights_tour_problem_on_a_chessboard import knight_summary, knight_summary_iterative
from factorization import build_spf, factor_spf, factor_iter, factor_recursive

import time

def time_second(functions):
    start_time = time.perf_counter()

    result=functions

    end_time = time.perf_counter()

    print(f"Время выполнения программы: {end_time - start_time:.6f} секунд")
    return functions


print("Рекурсия")
recursion=time_second(output_letter("Hello world"))
#
#
print("Задача о ханойской башне")
tower_list = {"hanoi_tower": (3,  "A", "C", "B")}
tower_of_hanoi_recursion = time_second(hanoi_tower(*tower_list["hanoi_tower"]))
tower_of_hanoi_iterative = time_second(hanoi_iterative(*tower_list["hanoi_tower"]))
#
#
print("Из рекурсивного в не рекурсивный подход")
parametr_a = 1
parametr_b = 5

recursive_to_non_recursive = time_second(sum_range(parametr_a, parametr_b))
recursive_to_non_recursive_while = time_second(sum_range_iter(parametr_a, parametr_b))
recursive_to_non_recursive_stack = time_second(sum_range_stack(parametr_a, parametr_b))
#
#
print("Рекурсивный поиск")
arg = [10, 23, 45, 70, 11, 15]
target = 15

recursion_a_search_method = time_second(search(arg, target))
#
#
print("Динамическое программирование, нахождение числа Фибоначчи тремя разными способами:")
numbers=20

dynamic_programming_naive = time_second(fib_naive(numbers))
dynamic_programming_memo = time_second(fib_memo(numbers))
dynamic_programming_tab = time_second(fib_tab(numbers))

#
#
print("Решение задачи обхода конём шахматной доски")
parametr_a=98
parametr_b=True

knights_tour_problem_on_a_chessboard = time_second(knight_summary(parametr_a, parametr_b))
knights_tour_problem_on_a_chessboard_neight = time_second(knight_summary(8, parametr_b))
knights_tour_problem_on_a_chessboard_iterative = time_second(knight_summary_iterative(parametr_a, parametr_b))

#
#
print("Факторизация")
spf = build_spf(100)
factorization_number = 60

factorization_iter = time_second(factor_iter(factorization_number))
factorization_recursive = time_second(factor_recursive(factorization_number))
factorization_spf = time_second(factor_spf(factorization_number, spf))
factorization_spf_neight = time_second(factor_spf(84, spf))
