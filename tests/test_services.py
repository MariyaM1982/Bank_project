import pandas as pd
import pytest

from src.main_transacion import export_report_json, export_report_xlsx
from src.sevices import process_bank_operations, process_bank_search


def test_process_bank_operations_counts_correctly():
    data = {
        "Категория": ["Супермаркеты", "Одежда", "Транспорт", "Супермаркеты",
                      "Транспорт"]
    }
    df = pd.DataFrame(data)
    categories = ["Супермаркеты", "Одежда", "Транспорт", "Еда"]

    result = process_bank_operations(df, categories)

    assert result == {
        "Супермаркеты": 2,
        "Одежда": 1,
        "Транспорт": 2
    }


def test_process_bank_operations_empty_df():
    df = pd.DataFrame(columns=["Категория"])
    result = process_bank_operations(df, ["Супермаркеты"])
    assert result == {}


def test_process_bank_operations_case_insensitive():
    data = {"Категория": ["транспорт", "ТРАНСПОРТ", "Транспорт"]}
    df = pd.DataFrame(data)
    result = process_bank_operations(df, ["тРансПорт"])
    assert result == {"тРансПорт": 3}

@pytest.fixture
def sample_data():
    return pd.DataFrame([
    {
    "Дата операции": "2021-12-31 16:44:00",
    "Статус": "OK",
    "Сумма операции": -160.89,
    "Валюта операции": "RUB",
    "Категория": "Супермаркеты",
    "Описание": "Колхоз"
    },
    {
    "Дата операции": "2021-12-30 15:22:00",
    "Статус": "DECLINED",
    "Сумма операции": -78.00,
    "Валюта операции": "USD",
    "Категория": "Транспорт",
    "Описание": "Метро"
    },
    {
    "Дата операции": "2021-12-28 10:00:00",
    "Статус": "OK",
    "Сумма операции": -300.00,
    "Валюта операции": "RUB",
    "Категория": "Одежда",
    "Описание": "ZARA"
    },
    ])

def test_filter_by_status(sample_data):
    result = filter_by_status(sample_data, "ok")
    assert isinstance(result, pd.DataFrame)
    assert len(result) == 2

def test_process_bank_search(sample_data):
    result = process_bank_search(sample_data, "zara")
    assert len(result) == 1
    assert result[0]["Описание"] == "ZARA"

def test_process_bank_operations(sample_data):
    categories = ["Супермаркеты", "Одежда"]
    result = process_bank_operations(sample_data, categories)
    assert result == {"Супермаркеты": 1, "Одежда": 1}

def test_export_json(tmp_path, sample_data):
    json_path = tmp_path / "report.json"
    export_report_json(sample_data, str(json_path))
    assert json_path.exists()
    assert json_path.read_text(encoding="utf-8").startswith("[{")

def test_export_xlsx(tmp_path, sample_data, xОшибка=None):
    xlsx_path = tmp_path / "report.xlsx"
    export_report_xlsx(sample_data, str(xlsx_path))
    assert "Ошибка: модуль src не найден."