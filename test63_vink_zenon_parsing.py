import json
import os
import pytest

# Путь к файлу JSON
FILE_PATH = r"C:/Users/annzi/Downloads/zenon_20250320_204243.json"

# Функция загрузки JSON
def load_json(file_path):
    """Загружает JSON-файл, если он существует"""
    assert os.path.exists(file_path), f"Файл {file_path} не найден!"
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

# Проверяем, доступен ли файл перед тестами
def test_file_exists():
    """Проверяет, что JSON-файл существует"""
    assert os.path.exists(FILE_PATH), f"Файл {FILE_PATH} не найден!"

# Тесты
def test_json_load():
    """Проверяет, что JSON-файл корректно загружается"""
    data = load_json(FILE_PATH)
    assert isinstance(data, list), "JSON должен содержать список товаров"
    assert len(data) > 0, "JSON не должен быть пустым"

@pytest.mark.parametrize("item", load_json(FILE_PATH) if os.path.exists(FILE_PATH) else [])
def test_product_fields(item):
    """Проверяет, что у каждого товара есть обязательные поля"""
    required_fields = ["product_code", "name", "price", "stocks"]
    for field in required_fields:
        assert field in item, f"Отсутствует поле {field} в товаре {item.get('product_code', 'Unknown')}"

def test_price_non_negative():
    """Проверяет, что цена неотрицательная"""
    data = load_json(FILE_PATH)
    for item in data:
        assert item["price"] >= 0, f"Цена отрицательная у товара {item['product_code']}"

def test_stock_quantity_non_negative():
    """Проверяет, что количество на складе неотрицательное"""
    data = load_json(FILE_PATH)
    for item in data:
        for stock in item.get("stocks", []):
            assert stock["quantity"] >= 0, f"Отрицательное количество у товара {item['product_code']} в складе {stock['stock']}"