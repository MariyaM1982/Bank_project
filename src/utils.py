import pandas as pd


def load_file(path: str, file_type: str) -> pd.DataFrame:
    """
    Загружает файл и возвращает DataFrame.
    """
    if file_type == "xlsx":
        df = pd.read_excel(path)
    elif file_type == "csv":
        df = pd.read_csv(path)
    elif file_type == "json":
        df = pd.read_json(path)
    else:
        raise ValueError("Неподдерживаемый формат файла")

    df["Дата операции"] = pd.to_datetime(df["Дата операции"])
    return df


def normalize_status(raw_status: str) -> str:
    """
    Преобразует статус из необработанного формата в верхний регистр.
    Пример: 'ok' -> 'EXECUTED'
    """
    mapping = {
        "ok": "EXECUTED",
        "executed": "EXECUTED",
        "canceled": "CANCELED",
        "pending": "PENDING",
    }
    return mapping.get(raw_status.strip().lower(), raw_status.strip().upper())
