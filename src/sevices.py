import re
from collections import Counter

import pandas as pd


def process_bank_search(df: pd.DataFrame, search: str) -> pd.DataFrame:
    """
    Фильтрует транзакции, в описании которых найдено ключевое слово (поиск через re).
    """
    pattern = re.compile(re.escape(search), re.IGNORECASE)
    return df[df["Описание"].apply(lambda x: bool(pattern.search(str(x))))]


def process_bank_operations(df: pd.DataFrame, categories: list[str]) -> dict:
    """
    Подсчитывает количество операций по указанным категориям.

    :param df: DataFrame с банковскими операциями
    :param categories: Список категорий для подсчета
    :return: Словарь {категория: количество}
    """
    result = Counter()

    for cat in categories:
        count = df["Категория"].apply(str.lower).tolist().count(cat.lower())
        if count > 0:
            result[cat] = count

    return dict(result)
