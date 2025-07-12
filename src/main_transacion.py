import logging
import re
from collections import Counter
import pandas as pd
from coverage import data


def process_bank_search(search: str) -> pd.DataFrame:
    """ " Фильтрует транзакции, содержащие поисковое слово в поле "Описание" """
    pattern = re.compile(re.escape(search), re.IGNORECASE)
    return data[data["Описание"].apply(lambda x: bool(pattern.search(str(x))))]


def process_bank_operations(data: pd.DataFrame, categories: list[str]) -> dict:
    """Подсчитывает количество транзакций по указанным категориям"""
    counts = Counter()
    for cat in categories:
        filtered = data["Категория"].str.lower().fillna("")
        counts[cat] = sum(filtered == cat.lower())
        return dict(counts)
    return None


def export_report_txt(data: pd.DataFrame, filepath: str = "report.txt") -> None:
    with open(filepath, "w", encoding="utf-8") as f:
        for _, row in data.iterrows():
            f.write(f"{row['Дата операции'].date()} {row['Описание']}\n")
            f.write(f"Карта: {row.get('Номер карты', 'N/A')}\n")
            f.write(f"Сумма: {abs(row['Сумма операции'])} {row['Валюта операции']}\n\n")


def export_report_json(data: pd.DataFrame, filepath: str = "report.json") -> None:
    data.to_json(filepath, orient="records", force_ascii=False, indent=2)


def export_report_xlsx(data: pd.DataFrame, filepath: str = "report.xlsx") -> None:
    data.to_excel(filepath, index=False)


def main():
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    ("1. Получить информацию о транзакциях из XLSX-файла")
    choice = input("Ваш выбор: ").strip()
    if choice != "1":
        print("Пока доступен только XLSX.")
        return
    file_path = input("Введите путь к файлу .xlsx: ").strip()
    try:
        df = pd.read_excel(file_path)
    except Exception as e:
        print(f"Ошибка загрузки: {e}")
        return

    available_statuses = df["Статус"].dropna().unique().tolist()
    available_statuses_lower = [s.lower() for s in available_statuses]
    while True:
        status = input(
            f"Введите статус для фильтрации (доступно: {', '.join(available_statuses)}): "
        ).strip()
        if status.lower() in available_statuses_lower:
            df = df[df["Статус"].str.lower() == status.lower()]
            break
        else:
            print(f"Статус '{status}' недоступен.")
        if input("Отсортировать операции по дате? Да/Нет: ").strip().lower() == "да":
            ascending = (
                input("По возрастанию или убыванию? ").strip().lower()
                == "по возрастанию"
            )
            df["Дата операции"] = pd.to_datetime(df["Дата операции"])
            df = df.sort_values(by="Дата операции", ascending=ascending)
        if (
            input("Выводить только рублевые транзакции? Да/Нет: ").strip().lower()
            == "да"
        ):
            df = df[df["Валюта операции"] == "RUB"]
        if input("Отфильтровать по слову в описании? Да/Нет: ").strip().lower() == "да":
            keyword = input("Введите ключевое слово: ").strip()
            df = process_bank_search(keyword)
        if df.empty:
            print("Не найдено ни одной транзакции по условиям фильтрации.")
            return
            print(f"Всего банковских операций в выборке: {len(df)}")
            print(
                df[
                    ["Дата операции", "Описание", "Сумма операции", "Валюта операции"]
                ].to_string(index=False)
            )
        if (
            input("Подсчитать количество операций по категориям? Да/Нет: ")
            .strip()
            .lower()
            == "да"
        ):
            cats = input("Введите категории через запятую: ").split(",")
            counts = process_bank_operations(df, [c.strip() for c in cats])
            print("Количество операций по категориям:")
    for cat, cnt in counts.items():
        print(f"{cat}: {cnt}")
    if input("Экспортировать результат в файл? Да/Нет: ").strip().lower() == "да":
        format_choice = input("Выберите формат: txt, json, xlsx: ").strip().lower()
    if format_choice == "json":
        export_report_json(df)
    elif format_choice == "xlsx":
        export_report_xlsx(df)
    else:
        export_report_txt(df)
        print("Файл успешно сохранён.")


if __name__ == "__main__":
    main()
