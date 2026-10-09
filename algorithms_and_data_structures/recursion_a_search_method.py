#2.4 Рекурсия как метод поиска 


def recursion_search(spisok, search_namespace, i=0):
    if i == len(spisok):
        return -1
    
    if spisok[i] == search_namespace:
        return i
    
    return recursion_search(spisok, search_namespace, i + 1)

def search(arg, target):

    result = recursion_search(arg, target)
    if result != -1:
        print(f"Элемент найден на индексе: {result}")
    else:
        print("Элемент не найден")


#
# Пример функции поиска элемента в списке с использованием рекурсии
#

arg = [10, 23, 45, 70, 11, 15]
target = 15

search(arg, target)

