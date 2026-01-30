import numpy as np
import time
from luckytools import LuckyTools

class Matrix:
    def __init__(self, size_x, size_y, size_z):
        global lt

        self.size_x = size_x
        self.size_y = size_y
        self.size_z = size_z
        self.data = np.random.randint(0, 100, (size_x, size_y, size_z))
        lt.print(f"Матрица {size_x}x{size_y}x{size_z} сгенерирована.", animate=True)

    def search_coordinates(self, target):
        coords = np.argwhere(self.data == target)
        if len(coords) > 0:
            lt.print(f"Найдено {len(coords)} вхождений числа {target}:", animate=True, time_show=0.1)
            for coord in coords:
                lt.print(f"  Координаты: {coord}", animate=True, time_show=0.1)
        else:
            lt.print(f"Число {target} не найдено.", animate=True, color="FF0000")
        return coords

    def measure_performance(self, target):
        start_time = time.time()
        self.search_coordinates(target)
        end_time = time.time()
        
        elapsed_time = end_time - start_time
        memory_usage = self.data.nbytes
        
        lt.print(f"Время выполнения: {elapsed_time:.6f} сек", animate=True)
        lt.print(f"Объем памяти матрицы: {memory_usage} байт", animate=True)
        return elapsed_time, memory_usage

    def compare_algorithms(self, target):
        lt.print("Сравнение алгоритмов...", animate=True)
        
        start_np = time.time()
        np.argwhere(self.data == target)
        end_np = time.time()
        time_np = end_np - start_np
        lt.print(f"Numpy поиск: {time_np:.6f} сек", animate=True)

        start_loop = time.time()
        found = []
        for x in range(self.size_x):
            for y in range(self.size_y):
                for z in range(self.size_z):
                    if self.data[x, y, z] == target:
                        found.append((x, y, z))
        end_loop = time.time()
        time_loop = end_loop - start_loop
        lt.print(f"Поиск перебором: {time_loop:.6f} сек", animate=True)
        
        if time_np < time_loop:
             lt.print("Нампай быстрее!", animate=True, color="00FF00")
        else:
             lt.print("Перебор быстрее!", animate=True, color="FFA500")

if __name__ == '__main__':
    lt = LuckyTools(prefix_name="⌊ Main ⌉ »", prefix_hex="00AAFF", prefix_short="⌊ 3D ⌉ »")
    
    try:
        size_input = lt.input("Введите размер матрицы: ")
        size = int(size_input) if size_input else 10
        
        matrix = Matrix(size, size, size)
        
        target_input = lt.input("Введите число для поиска: ")
        target = int(target_input) if target_input else 50
        
        matrix.search_coordinates(target)
        matrix.measure_performance(target)
        matrix.compare_algorithms(target)

    except ValueError:
        lt.print("Ошибка ввода", animate=True, color="FF0000")
