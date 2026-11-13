# for i in range(12, 3, -3):
#   print(i, end=' ')
#
# factorial=int(input())
##factorial=5
# resultat=1
# for i in range(1, factorial+1):
#    resultat= resultat * i
# print(resultat)

# number = int(input())
# result=0
# number_number=0
# while number != 0:
#    result+=number
#    number=int(input())
#    number_number+=1
# else:
#    print(number_number, result)
#
# number = int(input())
# number_two = 0
# number_number=0
# while number !=0:
#    number_two=int(input())
#    if number_two > number:
#        number_number+=1
#    number=number_two
# print(number_number)
#
# number_number=0
# number=int(input())
# number_two=0
# result=0
# while number !=0:
#    if number_number !=2:
#        result=number
#    number_two=int(input())
#    if number_two > result:
#        number_number+=1
#    number=number_two
# print(result)


# natura = int(input())
# natura_true = natura
# natura_two = 0
# while natura > 0:
#    natura_number = natura % 10
#    natura_two = natura_two * 10 + natura_number
#    natura //= 10
#
# print(natura_two)
#
# if natura_true == natura_two:
#    print('YES')
# else:
#    print('NO')

# def fib_naive(number: int):
#    if number <= 1:
#        return number
#    return fib_naive(number - 1) + fib_naive(number - 2)
# fibonachi=int(input())
# print(fib_naive(fibonachi))
# number_a = int(input())
# number_b = int(input())
# a=number_a
# b=number_b
# while b != 0:
#    a, b = b, a % b
# nok=number_a * number_b // a
# print(a, nok)

# number=int(input())
# if number == 1:
#    print('NEITHER')
# elif number % 2 == 0:
#    print("COMPOSITE")
# else:
#    is_prime=True
#    i = 3
#    while i*i <= number:
#        if number % i == 0:
#            is_prime=False
#            break
#        i += 2
#    if is_prime==False:
#        print("COMPOSITE")
#    else:
#        print("PRIME")

#spisok = []
#natura = int(input())
#
#while natura % 2 == 0:
#    spisok.append(2)
#    natura //= 2
#
#number = 3
#while number * number <= natura:
#    while natura % number == 0:
#        spisok.append(number)
#        natura //= number
#    number += 2
#if natura > 1:
#    spisok.append(natura)
#print(*spisok)

#n = int(input())
#m = int(input())
#
#number = 1
#
#for i in range(n):
#    if i % 2 == 0:
#        row = [str(x) for x in range(number, number  + m)]
#    else:
#        row = [str(x) for x in range(number + m - 1, number  - 1, -1)]
#    print(*row)
#    number += m