#2.3 Переход от рекурсивного к не рекурсивному решению


#
#Рекурсивная версия
#

def sum_range(a, b):
    if a > b:
        return 0
    return a + sum_range(a + 1, b)

#
#Преоброзвание в итеративную версию через цикл, хвостовая рекурсия
#

def sum_range_iter(a, b):
    total = 0
    while a <= b:
        total += a
        a += 1
    return total

#
#Преоброзование в итеративную версию через стек, не хвостовая рекурсия
#

def sum_range_stack(a, b):
    stack = [(a, b)]
    total = 0
    while stack:
        cur_a, cur_b = stack.pop()
        if cur_a > cur_b:
            continue
        # Эмуляция порядка: сначала обрабатываем «хвост», потом добавляем текущий элемент
        # В данном случае проще накапливать напрямую, но для демонстрации стека:
        total += cur_a
        stack.append((cur_a + 1, cur_b))
    return total


#
#Проверка работы функций
#
parametr_a = 1
parametr_b = 5

print(f"Рекурсивная версия: {sum_range(parametr_a, parametr_b)}")
print(f"Итеративная версия через цикл: {sum_range_iter(parametr_a, parametr_b)}")
print(f"Итеративная версия через стек: {sum_range_stack(parametr_a, parametr_b)}")