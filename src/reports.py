import pandas as pd


def sort_by_date(df: pd.DataFrame, ascending: bool = True) -> pd.DataFrame:
    """
    Сортирует DataFrame по дате операции.
    """
    return df.sort_values(by="Дата операции", ascending=ascending)


def filter_by_currency(df: pd.DataFrame, currency: str = "RUB") -> pd.DataFrame:
    """
    Оставляет только транзакции в указанной валюте.
    """
    return df[df["Валюта операции"].str.upper() == currency.upper()]


def export_report(df: pd.DataFrame, filepath: str = "report.txt") -> None:
    """
    Экспортирует список транзакций в текстовый файл.
    """
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"Всего банковских операций в выборке: {len(df)}\n\n")
        for _, row in df.iterrows():
            f.write(f"{row['Дата операции'].date()} {row['Описание']}\n")
            f.write(f"Сумма: {abs(row['Сумма операции'])} {row['Валюта операции']}\n\n")


def export_report_json(df: pd.DataFrame, filepath: str = "report.json") -> None:
    """
    Экспортирует транзакции в JSON-файл.
    """
    df.to_json(filepath, orient="records", force_ascii=False, indent=2)


def export_report_xlsx(df: pd.DataFrame, filepath: str = "report.xlsx") -> None:
    """
    Экспортирует транзакции в Excel-файл.
    """
    df.to_excel(filepath, index=False)
