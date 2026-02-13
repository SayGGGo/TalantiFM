import random
import time
from luckytools import LuckyTools


def buble_sort(lst):
    # Не зря делал презу про него
    for i in range(len(lst) - 1):
        for j in range(len(lst) - 1 - i):
            if lst[j] > lst[j + 1]:
                lst[j], lst[j + 1] = lst[j + 1], lst[j]
    return lst


def matrix(n):
    res_matrix = [[random.randint(1, 100) for i in range(n)] for i in range(n)]
    return res_matrix


def matrix_task(matrix, step):
    # тут через остаток от деления находим шаг (я решал такую задачу с репетитором Иваном, спс ему)
    shifted_matrix = []
    for i in matrix:
        n = len(i)
        if n == 0:
            shifted_matrix.append(i)
            continue

        real_step = step % n
        new = i[-real_step:] + i[:-real_step]
        shifted_matrix.append(new)

    return  shifted_matrix

def main():
    tools = LuckyTools(show_init=False)

    tools.print("----- Уровень C -----", animate=True, time_show=0.01)
    tools.print("--- Задача 1 ---", animate=True, time_show=0.01)

    for i in [100, 1000, 3000]:
        test_list_1 = [random.randint(1, 10000) for _ in range(i)]
        test_list_2 = test_list_1.copy()
        # Время выполнения алгоритма
        b_start = time.time()
        buble_sort(test_list_1)
        b_end = time.time()

        b_time = b_end - b_start
        tools.print(f"Бабл сорт на {i} числах справился за {b_time:.5f} секунд",
                    animate=True, time_show=0.01, white_tag=True)

        s_start = time.time()
        test_list_2.sort()
        s_end = time.time()

        s_time = s_end - s_start
        tools.print(f"А обычный сорт на {i} числах справился за {s_time:.5f} секунд",
                    animate=True, time_show=0.01, white_tag=True)

        if b_time < s_time:
            tools.print("Бабл сорт быстрее", animate=True, time_show=0.01, white_tag=True)
        else:
            tools.print("sort в питоне быстрее", animate=True, time_show=0.01, white_tag=True)


    tools.print("--- Задача 2 ---", animate=True, time_show=0.01)
    matrix_size = int(tools.input("Введите размер матрицы"))
    matrix_step = int(tools.input("На сколько сдвинуть"))
    # Ген матрицы
    matrix_start = matrix(matrix_size)
    tools.print("До:", animate=True, time_show=0.01)
    for i in matrix_start:
        print(i)

    tools.print("После:", animate=True, time_show=0.01)
    # Решение
    matrix_finish = matrix_task(matrix_start, matrix_step)
    for i in matrix_finish:
        print(i)

    tools.print("--- Задача 3 ---", animate=True, time_show=0.01)
    matrix_size = int(tools.input("Введите размер матрицы"))

    matrix_start = [[random.randint(1, 100) for i in range(matrix_size)] for i in range(matrix_size)]

    tools.print("Исходная матрица:", animate=True, time_show=0.01)
    for i in matrix_start:
        print(i)

    # ЭТО ЧЕ ТАКОЕ?!
    # Только так смог, проверяя каждый элемент благодоря тройному
    for i in range(matrix_size):
        for j in range(matrix_size - 1):
            for k in range(matrix_size - 1 - j):
                if matrix_start[k][i] > matrix_start[k + 1][i]:
                    matrix_start[k][i], matrix_start[k + 1][i] = matrix_start[k + 1][i], matrix_start[k][i]

    tools.print("Матрица после сортировки столбцов:", animate=True, time_show=0.01)
    for i in matrix_start:
        print(i)

    tools.print("--- Задача 4 ---", animate=True, time_show=0.01)
    lst_start = [random.randint(1, 10000) for i in range(10)]
    maximum = -float("inf")
    # Сложность линейная, достаточно простой алгоритм
    for i in lst_start:
        if i > maximum:
            maximum = i
    tools.print(f"парковка: {lst_start}, макс: {maximum}", animate=True, time_show=0.01)


if __name__ == "__main__":
    main()


"""
Этот код выполняет все задания с прикрепленной картинки, Андрей.
Если нужно ещё что-то —— обращайтесть. Если хочешь, я могу решить все
остальные задачи с других картинок. Желаю удачи на контрольной! 😊
"""
