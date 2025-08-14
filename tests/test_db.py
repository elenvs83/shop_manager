import sqlite3
import pandas as pd
import json
import sys
import shutil
import tempfile
import pytest
from pathlib import Path

import db as db_module


@pytest.fixture(autouse=True)
def temp_db(monkeypatch):
    """Создает временную базу данных для каждого теста."""
    tmp_dir = Path(tempfile.mkdtemp())
    tmp_db_path = tmp_dir / "test.db"

    # Патчим путь до базы
    monkeypatch.setattr(db_module, "DB_PATH", tmp_db_path)

    # Инициализируем БД
    db_module.init_db()

    yield tmp_db_path

    shutil.rmtree(tmp_dir)


def test_add_and_get_clients():
    cid = db_module.add_client("Иван", "ivan@example.com", "+79991234567", "Москва, ул. Пушкина")
    assert isinstance(cid, int)

    df = db_module.get_clients()
    assert len(df) == 1
    assert df.loc[0, "name"] == "Иван"


def test_add_and_get_products():
    pid = db_module.add_product("Товар 1", "SKU001", 199.99)
    assert isinstance(pid, int)

    df = db_module.get_products()
    assert len(df) == 1
    assert df.loc[0, "sku"] == "SKU001"


def test_add_and_get_orders():
    cid = db_module.add_client("Петр", "petr@example.com", "+79995554433", "СПб, Невский")
    pid = db_module.add_product("Товар 2", "SKU002", 299.99)

    oid = db_module.add_order(cid, pid, 3, "2025-01-01 10:00:00", "new")
    assert isinstance(oid, int)

    df = db_module.get_orders()
    assert len(df) == 1
    assert df.loc[0, "status"] == "new"


def test_export_import_csv(tmp_path):
    cid = db_module.add_client("Анна", "anna@example.com", "+79990001122", "Казань, Кремль")
    csv_file = tmp_path / "clients.csv"

    db_module.export_table_csv("clients", csv_file)
    assert csv_file.exists()

    # Очистим таблицу
    conn = sqlite3.connect(db_module.DB_PATH)
    conn.execute("DELETE FROM clients")
    conn.commit()
    conn.close()

    db_module.import_csv_to_table("clients", csv_file)
    df = db_module.get_clients()
    assert len(df) == 1
    assert df.loc[0, "name"] == "Анна"


def test_export_import_json(tmp_path):
    cid = db_module.add_client("Олег", "oleg@example.com", "+79998887766", "Самара")
    json_file = tmp_path / "clients.json"

    db_module.export_table_json("clients", json_file)
    assert json_file.exists()

    # Очистим таблицу
    conn = sqlite3.connect(db_module.DB_PATH)
    conn.execute("DELETE FROM clients")
    conn.commit()
    conn.close()

    db_module.import_json_to_table("clients", json_file)
    df = db_module.get_clients()
    assert len(df) == 1
    assert df.loc[0, "name"] == "Олег"
