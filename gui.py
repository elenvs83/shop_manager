"""
Tkinter GUI: вкладки Клиенты, Товары, Заказы, Аналитика.
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import date, datetime
from db import (
    add_client, get_clients, add_product, get_products, add_order, get_orders,
    export_table_csv as export_csv, export_table_json as export_json,
    import_csv_to_table, import_json_to_table
)
import analysis


class App(tk.Tk):
    """Главное окно приложения."""
    def __init__(self):
        super().__init__()
        self.title("Shop Manager")
        self.geometry("1000x700")

        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True)

        # вкладки
        self.clients_tab = ttk.Frame(notebook)
        self.products_tab = ttk.Frame(notebook)
        self.orders_tab = ttk.Frame(notebook)
        self.analysis_tab = ttk.Frame(notebook)

        notebook.add(self.clients_tab, text="Клиенты")
        notebook.add(self.products_tab, text="Товары")
        notebook.add(self.orders_tab, text="Заказы")
        notebook.add(self.analysis_tab, text="Аналитика")

        self._init_clients_tab()
        self._init_products_tab()
        self._init_orders_tab()
        self._init_analysis_tab()

        self.show_clients()
        self.show_products()
        self.show_orders()

    # === Клиенты ===
    def _init_clients_tab(self):
        frame = ttk.Frame(self.clients_tab)
        frame.pack(pady=10)

        ttk.Label(frame, text="Имя:").grid(row=0, column=0)
        self.client_name = tk.Entry(frame)
        self.client_name.grid(row=0, column=1)

        ttk.Label(frame, text="Email:").grid(row=1, column=0)
        self.email = tk.Entry(frame)
        self.email.grid(row=1, column=1)

        ttk.Label(frame, text="Телефон:").grid(row=2, column=0)
        self.phone = tk.Entry(frame)
        self.phone.grid(row=2, column=1)

        ttk.Label(frame, text="Адрес доставки:").grid(row=3, column=0)
        self.shipping_address = tk.Entry(frame)
        self.shipping_address.grid(row=3, column=1)

        ttk.Button(frame, text="Добавить клиента", command=self.add_client).grid(row=4, column=0, columnspan=2, pady=5)

        self.clients_list = tk.Listbox(self.clients_tab, width=70)
        self.clients_list.pack(pady=10)

        btn_frame = ttk.Frame(self.clients_tab)
        btn_frame.pack()

        ttk.Button(btn_frame, text="Обновить", command=self.show_clients).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="Экспорт CSV", command=lambda: self.export_data("clients", "csv")).grid(row=0, column=1, padx=5)
        ttk.Button(btn_frame, text="Экспорт JSON", command=lambda: self.export_data("clients", "json")).grid(row=0, column=2, padx=5)
        ttk.Button(btn_frame, text="Импорт CSV", command=lambda: self.import_data("clients", "csv")).grid(row=0, column=3, padx=5)
        ttk.Button(btn_frame, text="Импорт JSON", command=lambda: self.import_data("clients", "json")).grid(row=0, column=4, padx=5)

    def add_client(self):
        name = self.client_name.get()
        email = self.email.get()
        phone = self.phone.get()
        shipping_address = self.shipping_address.get()
        if name:
            add_client(name, email, phone, shipping_address)
            messagebox.showinfo("OK", "Клиент добавлен")
            self.show_clients()
            self.refresh_order_combos()

    def show_clients(self):
        self.clients_list.delete(0, tk.END)
        df = get_clients()
        for _, row in df.iterrows():
            self.clients_list.insert(tk.END, f"{row['name']} - {row['email']} - {row['phone']} - {row['shipping_address']}")

    # === Товары ===
    def _init_products_tab(self):
        frame = ttk.Frame(self.products_tab)
        frame.pack(pady=10)

        ttk.Label(frame, text="Название:").grid(row=0, column=0)
        self.product_name = tk.Entry(frame)
        self.product_name.grid(row=0, column=1)

        ttk.Label(frame, text="Артикул:").grid(row=1, column=0)
        self.sku = tk.Entry(frame)
        self.sku.grid(row=1, column=1)

        ttk.Label(frame, text="Цена:").grid(row=2, column=0)
        self.product_price = tk.Entry(frame)
        self.product_price.grid(row=2, column=1)

        ttk.Button(frame, text="Добавить товар", command=self.add_product).grid(row=3, column=0, columnspan=2, pady=5)

        self.products_list = tk.Listbox(self.products_tab, width=50)
        self.products_list.pack(pady=10)

        btn_frame = ttk.Frame(self.products_tab)
        btn_frame.pack()

        ttk.Button(btn_frame, text="Обновить", command=self.show_products).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="Экспорт CSV", command=lambda: self.export_data("products", "csv")).grid(row=0, column=1, padx=5)
        ttk.Button(btn_frame, text="Экспорт JSON", command=lambda: self.export_data("products", "json")).grid(row=0, column=2, padx=5)
        ttk.Button(btn_frame, text="Импорт CSV", command=lambda: self.import_data("products", "csv")).grid(row=0, column=3, padx=5)
        ttk.Button(btn_frame, text="Импорт JSON", command=lambda: self.import_data("products", "json")).grid(row=0, column=4, padx=5)

    def add_product(self):
        name = self.product_name.get()
        sku = self.sku.get()
        try:
            price = float(self.product_price.get())
        except ValueError:
            messagebox.showerror("Ошибка", "Цена должна быть числом")
            return
        add_product(name, sku, price)
        messagebox.showinfo("OK", "Товар добавлен")
        self.show_products()
        self.refresh_order_combos()

    def show_products(self):
        self.products_list.delete(0, tk.END)
        df = get_products()
        for _, row in df.iterrows():
            self.products_list.insert(tk.END, f"{row['name']} - {row['sku']} — {row['price']} руб.")

    # === Заказы ===
    def _init_orders_tab(self):
        frame = ttk.Frame(self.orders_tab)
        frame.pack(pady=10)

        self.client_combo = ttk.Combobox(frame, values=list(get_clients()["name"]))
        self.client_combo.grid(row=0, column=0, padx=5)
        self.product_combo = ttk.Combobox(frame, values=list(get_products()["name"]))
        self.product_combo.grid(row=0, column=1, padx=5)

        self.qty_entry = tk.Entry(frame, width=5)
        self.qty_entry.grid(row=0, column=2, padx=5)
        self.qty_entry.insert(0, "1")

        ttk.Label(frame, text="Статус:").grid(row=0, column=3)
        self.status_entry = tk.Entry(frame)
        self.status_entry.grid(row=0, column=4)

        ttk.Button(frame, text="Создать заказ", command=self.add_order).grid(row=0, column=5, padx=5)

        # --- Панель фильтров ---
        filter_frame = ttk.Frame(self.orders_tab)
        filter_frame.pack(pady=5)

        ttk.Label(filter_frame, text="Клиент:").grid(row=0, column=0, padx=5)
        self.filter_client = ttk.Combobox(filter_frame, values=[""] + list(get_clients()["name"]))
        self.filter_client.grid(row=0, column=1, padx=5)

        ttk.Label(filter_frame, text="Дата (YYYY-MM-DD):").grid(row=0, column=2, padx=5)
        self.filter_date = tk.Entry(filter_frame, width=12)
        self.filter_date.grid(row=0, column=3, padx=5)

        ttk.Button(filter_frame, text="Фильтровать", command=self.filter_orders).grid(row=0, column=4, padx=5)
        ttk.Button(filter_frame, text="Сброс", command=self.show_orders).grid(row=0, column=5, padx=5)

        # --- Список заказов ---
        self.orders_list = tk.Listbox(self.orders_tab, width=70)
        self.orders_list.pack(pady=10)

        btn_frame = ttk.Frame(self.orders_tab)
        btn_frame.pack()

        ttk.Button(btn_frame, text="Обновить", command=self.show_orders).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="Экспорт CSV", command=lambda: self.export_data("orders", "csv")).grid(row=0, column=1, padx=5)
        ttk.Button(btn_frame, text="Экспорт JSON", command=lambda: self.export_data("orders", "json")).grid(row=0, column=2, padx=5)
        ttk.Button(btn_frame, text="Импорт CSV", command=lambda: self.import_data("orders", "csv")).grid(row=0, column=3, padx=5)
        ttk.Button(btn_frame, text="Импорт JSON", command=lambda: self.import_data("orders", "json")).grid(row=0, column=4, padx=5)

    def add_order(self):
        client_name = self.client_combo.get()
        product_name = self.product_combo.get()
        qty = int(self.qty_entry.get())
        created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        status = self.status_entry.get() or "в ожидании"

        clients_df = get_clients()
        products_df = get_products()

        client_id = clients_df.loc[clients_df["name"] == client_name, "client_id"].iloc[0]
        product_id = products_df.loc[products_df["name"] == product_name, "product_id"].iloc[0]

        add_order(int(client_id), int(product_id), int(qty), created_at, status)
        messagebox.showinfo("OK", "Заказ добавлен")
        self.show_orders()

    def show_orders(self):
        self.orders_list.delete(0, tk.END)
        orders_df = get_orders()
        clients_df = get_clients()
        products_df = get_products()

        self.filter_client.set("")
        self.filter_date.delete(0, tk.END)

        for _, row in orders_df.iterrows():
            try:
                client = clients_df.loc[clients_df["client_id"] == row["client_id"], "name"].iloc[0]
                product = products_df.loc[products_df["product_id"] == row["product_id"], "name"].iloc[0]
                self.orders_list.insert(tk.END, f"{row['created_at']} — {client} заказ {row['quantity']} × {product} (статус: {row['status']})")
            except Exception as e:
                print("Ошибка при отображении заказа:", e)

    def filter_orders(self):
        client_filter = self.filter_client.get().strip()
        date_filter = self.filter_date.get().strip()

        orders_df = get_orders()
        clients_df = get_clients()
        products_df = get_products()

        if client_filter:
            client_ids = clients_df.loc[clients_df["name"] == client_filter, "client_id"].tolist()
            orders_df = orders_df[orders_df["client_id"].isin(client_ids)]

        if date_filter:
            orders_df = orders_df[orders_df["created_at"].str.contains(date_filter)]

        self.orders_list.delete(0, tk.END)
        for _, row in orders_df.iterrows():
            try:
                client = clients_df.loc[clients_df["client_id"] == row["client_id"], "name"].iloc[0]
                product = products_df.loc[products_df["product_id"] == row["product_id"], "name"].iloc[0]
                self.orders_list.insert(tk.END, f"{row['created_at']} — {client} заказ {row['quantity']} × {product} (статус: {row['status']})")
            except Exception as e:
                print("Ошибка при отображении заказа:", e)

    # === Аналитика ===
    def _init_analysis_tab(self):
        ttk.Button(self.analysis_tab, text="Топ клиентов", command=analysis.show_top_clients).pack(pady=5)
        ttk.Button(self.analysis_tab, text="Динамика заказов", command=analysis.show_orders_over_time).pack(pady=5)
        ttk.Button(self.analysis_tab, text="Граф связей", command=analysis.show_client_graph).pack(pady=5)

    # === Импорт / экспорт ===
    def export_data(self, table, fmt):
        filename = filedialog.asksaveasfilename(defaultextension=f".{fmt}")
        if filename:
            if fmt == "csv":
                export_csv(table, filename)
            else:
                export_json(table, filename)
            messagebox.showinfo("OK", f"{table} экспортирован в {filename}")

    def import_data(self, table, fmt):
        filename = filedialog.askopenfilename(filetypes=[(fmt.upper(), f"*.{fmt}")])
        if filename:
            if fmt == "csv":
                import_csv_to_table(table, filename)
            else:
                import_json_to_table(table, filename)
            messagebox.showinfo("OK", f"{table} импортирован из {filename}")
            self.refresh_order_combos()

    def refresh_order_combos(self):
        clients_df = get_clients()
        products_df = get_products()
        self.client_combo['values'] = list(clients_df["name"])
        self.product_combo['values'] = list(products_df["name"])
        self.filter_client['values'] = [""] + list(clients_df["name"])


if __name__ == "__main__":
    app = App()
    app.mainloop()
