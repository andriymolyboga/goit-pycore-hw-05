def caching_fibonacci():
    # Створюємо кеш для зберігання результатів
    cache = {0: 0, 1: 1}

    def fibonacci(n):
        # Перевіряємо, чи є результат у кеші
        if n in cache:
            return cache[n]

        # Якщо результату немає, обчислюємо його рекурсивно
        cache[n] = fibonacci(n - 1) + fibonacci(n - 2)

        return cache[n]

    # Повертаємо внутрішню функцію
    return fibonacci


# Отримуємо функцію fibonacci
fib = caching_fibonacci()

print(fib(10))  # 55
print(fib(15))  # 610
