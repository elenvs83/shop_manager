import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx
from db import DB_PATH

def _read_sql(query: str):
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql(query, conn)
    conn.close()
    return df

def show_top_clients():
    query = """
    SELECT c.name, COUNT(o.order_id) AS total_orders
    FROM orders o
    JOIN clients c ON o.client_id = c.client_id
    GROUP BY c.client_id
    ORDER BY total_orders DESC
    LIMIT 5
    """
    df = _read_sql(query)
    if df.empty:
        print("Нет данных для анализа")
        return
    plt.figure(figsize=(8, 5))
    sns.barplot(x="total_orders", y="name", data=df)
    plt.title("Топ 5 клиентов по количеству заказов")
    plt.xlabel("Количество заказов")
    plt.ylabel("Клиент")
    plt.tight_layout()
    plt.show()

def show_orders_over_time():
    query = "SELECT created_at FROM orders"
    df = _read_sql(query)
    if df.empty:
        print("Нет данных для анализа")
        return
    df["created_at"] = pd.to_datetime(df["created_at"])
    series = df.groupby(df["created_at"].dt.date).size()
    plt.figure(figsize=(10, 5))
    series.plot(kind="line", marker="o")
    plt.title("Динамика количества заказов")
    plt.xlabel("Дата")
    plt.ylabel("Количество заказов")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def show_client_graph():
    query = """
    SELECT c.name AS client, p.name AS product
    FROM orders o
    JOIN clients c ON o.client_id = c.client_id
    JOIN products p ON o.product_id = p.product_id
    """
    df = _read_sql(query)
    if df.empty:
        print("Нет данных для анализа")
        return

    G = nx.Graph()
    for _, row in df.iterrows():
        G.add_edge(row["client"], row["product"])

    plt.figure(figsize=(10, 7))
    pos = nx.spring_layout(G, seed=42)
    nx.draw(G, pos, with_labels=True, node_color="lightblue", font_size=8, edge_color="gray")
    plt.title("Граф связей клиентов и товаров")
    plt.show()
