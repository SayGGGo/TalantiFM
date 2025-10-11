import random

def task1(n):
    matrix_gen = []
    for i in range(n):
        matrix_string = []
        for j in range(n):
            if n-i-1==j:
                matrix_string.append("1")
            else:
                if n - (i) - 1 > j:
                    matrix_string.append("0")
                else:
                    if n - (i) - 1 < j:
                        matrix_string.append("2")
        matrix_gen.append(matrix_string)

    for row in matrix_gen:
        for element in row:
            print(element, end='\t')
        print()


def task2(n):
    matrix_gen = []
    for i in range(n):
        matrix_string = []
        for j in range(n):
            if n-i-1==j:
                matrix_string.append("0")
            else:
                for num in range(1, n):
                    if n - (i+num) - 1 == j or n - (i-num) - 1 == j:
                        matrix_string.append(num)
        matrix_gen.append(matrix_string)

    for row in matrix_gen:
        for element in row:
            print(element, end='\t')
        print()

def task3(n,m):
    matrix_gen = []
    status = 0
    for i in range(n):
        matrix_string = []
        for j in range(m):
            if status == 0:
                matrix_string.append(".")
                status = 1
            else:
                matrix_string.append("*")
                status = 0
        matrix_gen.append(matrix_string)

    for row in matrix_gen:
        for element in row:
            print(element, end='\t')
        print()

number = int(input("[TASK 1] Введите n > "))
task1(number)
number = int(input("[TASK 2] Введите n > "))
task2(number)
number = int(input("[TASK 3] Введите n > "))
number_m = int(input("[TASK 3] Введите m > "))
task3(number, number_m)

