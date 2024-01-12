arithmetic_mean = lambda x, y: (x + y) / 2
arithmetic_mean.__name__ = "Арифметичний"
geometric_mean = lambda x, y: (x * y) ** 0.5
geometric_mean.__name__ = "Геометричний"
harmonic_mean = lambda x, y: 2 / ((1 / x) + (1 / y))
harmonic_mean.__name__ = "Гармонічний"


def find_min_mean(x, y):
    mean_functions = [arithmetic_mean, geometric_mean, harmonic_mean]
    min_mean = min(mean_func(x, y) for mean_func in mean_functions)
    min_mean_algorithm = [func.__name__ for func in mean_functions if func(x, y) == min_mean][0]
    print(f"Мінімальне середнє значення ({min_mean:.2f}) за алгоритмом {min_mean_algorithm}")


def main() -> None:
    find_min_mean(3, 9)

    
if __name__ == '__main__': main()