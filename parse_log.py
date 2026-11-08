import sys
from collections import Counter


def parse_log_line(line: str) -> dict:
    """
    Розбирає один рядок лог-файлу на компоненти.
    """
    parts = line.split(maxsplit=3)

    if len(parts) != 4:
        raise ValueError("Неправильний формат рядка логу")

    date, time, level, message = parts

    if level not in ("INFO", "ERROR", "DEBUG", "WARNING"):
        raise ValueError(f"Невідомий рівень логування: {level}")

    return {
        "date": date,
        "time": time,
        "level": level,
        "message": message.strip()
    }


def load_logs(file_path: str) -> list:
    """
    Завантажує та парсить записи з файлу.
    """
    logs = []

    with open(file_path, "r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            if not line.strip():
                continue

            try:
                logs.append(parse_log_line(line))
            except ValueError as error:
                print(
                    f"Помилка у рядку {line_number}: {error}",
                    file=sys.stderr
                )

    return logs


def filter_logs_by_level(logs: list, level: str) -> list:
    """
    Повертає записи тільки заданого рівня логування.
    """
    return list(filter(
        lambda log: log["level"] == level.upper(),
        logs
    ))


def count_logs_by_level(logs: list) -> dict:
    """
    Підраховує кількість записів кожного рівня.
    """
    counts = Counter(log["level"] for log in logs)

    return {
        level: counts[level]
        for level in ("INFO", "DEBUG", "ERROR", "WARNING")
    }


def display_log_counts(counts: dict):
    """
    Виводить статистику у вигляді таблиці.
    """
    print(f"{'Рівень логування':<20} | {'Кількість':>10}")
    print("-" * 35)

    for level, count in counts.items():
        print(f"{level:<20} | {count:>10}")


def main():
    """
    Головна функція програми.
    """
    if len(sys.argv) < 2:
        print("Використання: python main.py <шлях_до_файлу> [рівень]")
        return

    file_path = sys.argv[1]

    try:
        logs = load_logs(file_path)

        counts = count_logs_by_level(logs)
        display_log_counts(counts)

        if len(sys.argv) >= 3:
            level = sys.argv[2].upper()

            if level not in ("INFO", "ERROR", "DEBUG", "WARNING"):
                print(f"\nНевідомий рівень логування: {level}")
                return

            filtered_logs = filter_logs_by_level(logs, level)

            print(f"\nДеталі логів для рівня '{level}':")

            for log in filtered_logs:
                print(
                    f"{log['date']} {log['time']} - {log['message']}"
                )

    except FileNotFoundError:
        print(f"Помилка: файл '{file_path}' не знайдено.")

    except PermissionError:
        print(f"Помилка: немає дозволу на читання файлу '{file_path}'.")

    except OSError as error:
        print(f"Помилка читання файлу: {error}")


if __name__ == "__main__":
    main()
