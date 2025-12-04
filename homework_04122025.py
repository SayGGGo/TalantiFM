# Homework 04.12.2025 - Generators / Андрей Сайгин ИИ-71
from math import sqrt

def task_1(n):
    gen = ["четное" if i % 2 == 0 else "нечетное" for i in range(0, n + 1)]
    return gen


def task_2(n):
    gen = ["FizzBuzz" if i % 3 == 0 and i % 5 == 0 else "Fizz" if i % 3 == 0 else "Buzz" if i % 5 == 0 else i for i in range(1, 101)]
    return gen


def task_3(n):
    gen = [i if i > 10 else 0 for i in range(0, n + 1)]
    return gen


def task_4(n):
    gen = {i: ("even" if i % 2 == 0 else "odd") for i in range(1, n + 1)}
    return gen


def task_5(lst):
    gen = [len(s) if len(s) <= 5 else 5 for s in lst]
    return gen


def task_6(lst):
    gen = [x if x > 0 else 0 for x in lst]
    return gen


def task_7(lst):
    gen = [sqrt(x) if x > 0 else 0 for x in lst]
    return gen


def task_8(lst):
    gen = [x * x if x % 2 == 0 else x * x * x for x in lst]
    return gen


def task_9(lst):
    gen = ["High" if x > 50 else "Medium" if x >= 20 else "Low" for x in lst]
    return gen
