import time
import random


def bruteforce(lst, k):
    for i in range(len(lst)):
        if lst[i] >= k:
            return i
    return len(lst)


def binary_search(lst, k):
    low = 0
    high = len(lst) - 1
    while low <= high:
        middle = (low + high) // 2
        if lst[middle] >= k:
            high = middle - 1
        else:
            low = middle + 1
    return low


def recursion(lst, k, i=0):
    if i == len(lst) or lst[i] >= k:
        return i
    return recursion(lst, k, i + 1)


def rand(lst, k):
    find_list = lst
    find_list.append(k)
    find_list.sort()
    while True:
        gen_list = [random.randint(min(find_list), max(find_list)) for i in range(len(find_list))]
        gen_list.sort()
        if gen_list == find_list:
            # print(f"+ Попадение | {gen_list}")
            return gen_list
        # print(f"- Не попал | {gen_list} != {find_list}")

lst = [random.randint(0, 50) for i in range(5)]
lst.sort()
k = random.randint(0, 25)

start = time.perf_counter()
bruteforce(lst, k)
end = time.perf_counter()
print(f"Брутфорс: {end - start:0.8f}")

start = time.perf_counter()
binary_search(lst, k)
end = time.perf_counter()
print(f"Бинарный поиск: {end - start:0.8f}")

start = time.perf_counter()
recursion(lst, k)
end = time.perf_counter()
print(f"Рекурсия: {end - start:0.8f}")

# O(n log n), не смотря на то, какой алгоритм очень тупой
start = time.perf_counter()
rand(lst, k)
end = time.perf_counter()
print(f"Да ты снайпер: {end - start:0.8f}")