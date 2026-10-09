#2.2 Задача ханойской башни


#
#Рекурсивное решение задачи ханойской башни 
#
def hanoi_tower(n, start, end, aux):
    try:
        if n >= 1000:
            raise RecursionError
        if n == 1:
            print(f"Перемещаем диск 1 со стержня {start} на стержень {end}")
            return
        hanoi_tower(n - 1, start, aux, end)
        print(f"Перемещаем диск {n} со стержня {start} на стержень {end}")
        hanoi_tower(n - 1, aux, end, start)
    except RecursionError:
        print("Превышен предел рекурсии")



#
#Итеративное решение задачи ханойской башни
#
def hanoi_iterative(n, start, end, aux):
    # Если количество дисков чётное, меняем местами end и aux,
    # чтобы наименьший диск двигался по кругу в нужном направлении
    if n % 2 == 0:
        end, aux = aux, end

    # Инициализируем стержни: на start диски от n до 1 (сверху вниз)
    rods = {
        start: list(range(n, 0, -1)),
        end: [],
        aux: [],
    }

    total_moves = (1 << n) - 1  # 2^n - 1

    def make_move(src, dst):
        """Выполняет один допустимый ход между src и dst"""
        # Если один из стержней пуст, берём диск с непустого
        if not rods[src]:
            disk = rods[dst].pop()
            rods[src].append(disk)
            print(f"Переместить диск {disk} со стержня {dst} на стержень {src}")
        elif not rods[dst]:
            disk = rods[src].pop()
            rods[dst].append(disk)
            print(f"Переместить диск {disk} со стержня {src} на стержень {dst}")
        # Если оба непустые, кладём меньший диск на больший
        elif rods[src][-1] > rods[dst][-1]:
            disk = rods[dst].pop()
            rods[src].append(disk)
            print(f"Переместить диск {disk} со стержня {dst} на стержень {src}")
        else:
            disk = rods[src].pop()
            rods[dst].append(disk)
            print(f"Переместить диск {disk} со стержня {src} на стержень {dst}")

    for i in range(1, total_moves + 1):
        if i % 3 == 1:
            make_move(start, end)
        elif i % 3 == 2:
            make_move(start, aux)
        else:
            make_move(aux, end)


#
#Проверка работы функций
#

tower_list = {"hanoi_tower": (3,  "A", "C", "B")}

print("Входные данные:")
print(*tower_list['hanoi_tower'])

print("Рекурсивное решение задачи ханойской башни:")
hanoi_tower(*tower_list["hanoi_tower"])

print("Итеративное решение задачи ханойской башни:")
hanoi_iterative(*tower_list["hanoi_tower"])


