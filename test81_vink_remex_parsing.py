import json
import os
import pytest
import logging

# Настройка логирования
LOG_FILE = "logs/test_parser.log"
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Путь к файлу JSON (замени на свой)
FILE_PATH = r"C:/Users/annzi/Downloads/remex_20250321_082747.json"

@pytest.fixture
def load_json():
    """Фикстура для загрузки JSON-файла"""
    assert os.path.exists(FILE_PATH), f"Файл {FILE_PATH} не найден!"

    with open(FILE_PATH, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
            assert isinstance(data, list), "Ошибка: JSON должен быть списком товаров!"
            assert len(data) > 0, "Ошибка: JSON-файл пустой!"
            return data
        except json.JSONDecodeError:
            pytest.fail("Ошибка декодирования JSON! Файл поврежден.")

def test_file_exists():
    """Проверяет, что JSON-файл существует"""
    assert os.path.exists(FILE_PATH), f"Файл {FILE_PATH} не найден!"
    logging.info("✅ Файл JSON найден.")

def test_json_load(load_json):
    """Проверяет, что JSON-файл корректно загружается"""
    logging.info("✅ JSON-файл успешно загружен.")

def test_product_fields(load_json):
    """Проверяет, что у каждого товара есть обязательные поля"""
    required_fields = ["product_code", "name", "price", "stocks"]
    errors = []

    for idx, item in enumerate(load_json):
        missing_fields = [field for field in required_fields if field not in item or item[field] in [None, "", []]]
        if missing_fields:
            errors.append(f"Запись {idx + 1}: отсутствуют поля {missing_fields} -> {item}")