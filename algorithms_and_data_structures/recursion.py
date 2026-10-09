#2.1 Рекурсия


def internal_function(parametr, index=0):
    if index == len(parametr):
        return
    if parametr[index] == " ":
        print("Пробел")
        return internal_function(parametr, index + 1)
    print(f"Текущий символ: {parametr[index]}")
    return internal_function(parametr, index + 1)

def  output_letter(*args): #Валидация
    try:
        if len(args) != 1:
            print("Ошибка: функция принимает только один параметр")
            return
        return internal_function(args[0])
    except TypeError:
        print("Ошибка: передана не строка")


#
#Проверка работы функции
#

output_letter("Hello world")

output_letter(10)
