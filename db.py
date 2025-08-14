"""
Работа с SQLite: схема, CRUD, импорт/экспорт CSV и JSON.
"""
import sqlite3
import pandas as pd
import json
from pathlib import Path

DB_PATH = Path(__file__).parent / 'data' / 'shop.db'
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

def get_conn():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_conn()
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS clients (
            client_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            shipping_address TEXT NOT NULL
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS products (
            product_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            sku TEXT NOT NULL,
            price REAL NOT NULL
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            created_at TEXT NOT NULL,
            status TEXT NOT NULL,
            FOREIGN KEY(client_id) REFERENCES clients(client_id),
            FOREIGN KEY(product_id) REFERENCES products(product_id)
        )
    """)
    conn.commit()
    conn.close()

def add_client(name, email, phone, shipping_address):
    conn = get_conn()
    c = conn.cursor()
    c.execute("INSERT INTO clients (name, email, phone, shipping_address) VALUES (?, ?, ?, ?)", (name, email, phone, shipping_address))
    conn.commit()
    cid = c.lastrowid
    conn.close()
    return cid

def get_clients():
    conn = get_conn()
    df = pd.read_sql('SELECT * FROM clients', conn)
    conn.close()
    return df

def add_product(name, sku, price):
    conn = get_conn()
    c = conn.cursor()
    c.execute("INSERT INTO products (name, sku, price) VALUES (?, ?, ?)", (name, sku, price))
    conn.commit()
    pid = c.lastrowid
    conn.close()
    return pid

def get_products():
    conn = get_conn()
    df = pd.read_sql('SELECT * FROM products', conn)
    conn.close()
    return df

def add_order(client_id, product_id, quantity, created_at, status):
    conn = get_conn()
    c = conn.cursor()
    c.execute("INSERT INTO orders (client_id, product_id, quantity, created_at, status) VALUES (?, ?, ?, ?, ?)",
              (client_id, product_id, quantity, created_at, status))
    conn.commit()
    oid = c.lastrowid
    conn.close()
    return oid

def get_orders():
    conn = get_conn()
    df = pd.read_sql('SELECT * FROM orders ORDER BY created_at DESC', conn)
    conn.close()
    return df

def export_table_csv(table, filename):
    conn = get_conn()
    df = pd.read_sql(f"SELECT * FROM {table}", conn)
    df.to_csv(filename, index=False)
    conn.close()

def export_table_json(table, filename):
    conn = get_conn()
    df = pd.read_sql(f"SELECT * FROM {table}", conn)
    df.to_json(filename, orient="records", force_ascii=False)
    conn.close()

def import_csv_to_table(table, filename):
    df = pd.read_csv(filename)
    conn = get_conn()
    df.to_sql(table, conn, if_exists="append", index=False)
    conn.close()

def import_json_to_table(table, filename):
    with open(filename, encoding="utf-8") as f:
        data = json.load(f)
    df = pd.DataFrame(data)
    conn = get_conn()
    df.to_sql(table, conn, if_exists="append", index=False)
    conn.close()
