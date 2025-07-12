import logging
import re
from pathlib import Path
import pandas as pd

from src.logging_config import setup_logger
from src.reports import (
    export_report,
    export_report_json,
    export_report_xlsx,
    filter_by_currency,
    sort_by_date,
)
from src.sevices import process_bank_search
from src.utils import load_file, normalize_status


def main():
    setup_logger()
    logging.info("Программа запущена")
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    file_type = input("Пользователь: ")
    file_map = {"1": "json", "2": "csv", "3": "xlsx"}

    if file_type not in file_map:
        print("Неверный выбор. Завершение работы.")
        return

    file_ext = file_map[file_type]
    print(f"Для обработки выбран {file_ext.upper()}-файл.")

    path = input("Введите путь к файлу: ")
    if not Path(path).exists():
        print("Файл не найден. Завершение.")
        return

    try:
        data = load_file(path, file_ext)
    except Exception as e:
        print(f"Ошибка загрузки файла: {e}")
        return

    # Статусы
    valid_statuses = ["EXECUTED", "CANCELED", "PENDING"]
    while True:
        status = input(
            "Введите статус для фильтрации (EXECUTED, CANCELED, PENDING): "
        ).upper()
        if status in valid_statuses:
            break
        logging.info(f"Пользователь выбрал статус: {status}")
        print(f'Статус "{status}" недоступен. Повторите ввод.')

    data = data[data["Статус"].apply(lambda x: normalize_status(x)) == status]
    print(f'Операции отфильтрованы по статусу "{status}"')

    # Сортировка
    sort = input("Отсортировать операции по дате? Да/Нет: ").strip().lower()
    if sort == "да":
        direction = (
            input("Отсортировать по возрастанию или по убыванию? ").strip().lower()
        )
        ascending = direction == "по возрастанию"
        data = sort_by_date(data, ascending)

    # Рубли
    if input("Выводить только рублевые транзакции? Да/Нет: ").strip().lower() == "да":
        data = filter_by_currency(data, "RUB")

    # Поиск по описанию
    if input("Отфильтровать по слову в описании? Да/Нет: ").strip().lower() == "да":
        keyword = input("Введите слово для поиска в описании: ").strip()
        data = process_bank_search(data, keyword)

    # Вывод
    if data.empty:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации.")
    else:
        print("Распечатываю итоговый список транзакций...\n")
        print(f"Всего банковских операций в выборке: {len(data)}\n")
        for _, row in data.iterrows():
            print(f"{row['Дата операции'].date()} {row['Описание']}")
            print(f"Сумма: {abs(row['Сумма операции'])} {row['Валюта операции']}")
            print()

    if input("Экспортировать результат в файл? Да/Нет: ").strip().lower() == "да":
        export_report(data)
        print("Результаты экспортированы в report.txt")
        logging.info("Результаты экспортированы в report.txt")

    if input("Экспортировать результат в файл? Да/Нет: ").strip().lower() == "да":
        format_choice = input("Выберите формат: txt, json, xlsx: ").strip().lower()
        if format_choice == "json":
            export_report_json(data)
            logging.info("Результаты экспортированы в report.json")
        elif format_choice == "xlsx":
            export_report_xlsx(data)
            logging.info("Результаты экспортированы в report.xlsx")
        else:
            export_report(data)
            logging.info("Результаты экспортированы в report.txt")


if __name__ == "__main__":
    main()
