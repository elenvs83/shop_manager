import builtins
import pytest
from unittest.mock import patch, MagicMock
import pandas as pd

@pytest.fixture
def app():
    # Мокаем Tkinter и messagebox/filedialog
    with patch("tkinter.Tk.__init__", return_value=None), \
         patch("tkinter.Entry"), \
         patch("tkinter.Listbox"), \
         patch("tkinter.ttk.Combobox"), \
         patch("tkinter.ttk.Frame"), \
         patch("tkinter.ttk.Button"), \
         patch("tkinter.ttk.Label"), \
         patch("tkinter.ttk.Notebook"), \
         patch("tkinter.ttk.LabelFrame"), \
         patch("tkinter.messagebox.showinfo"), \
         patch("tkinter.messagebox.showerror"), \
         patch("tkinter.filedialog.asksaveasfilename", return_value="test.csv"), \
         patch("tkinter.filedialog.askopenfilename", return_value="test.csv"), \
         patch("db.get_clients", return_value=pd.DataFrame([{
             "client_id": 1, "name": "Client1", "email": "c1@x.com",
             "phone": "123", "shipping_address": "Addr1"
         }])), \
         patch("db.get_products", return_value=pd.DataFrame([{
             "product_id": 2, "name": "Product1", "sku": "sku1", "price": 10.0
         }])), \
         patch("db.get_orders", return_value=pd.DataFrame([{
             "client_id": 1, "product_id": 2, "quantity": 3, "created_at": "2025-08-01"
         }])), \
         patch("db.add_client"), patch("db.add_product"), patch("db.add_order"), \
         patch("db.export_table_csv"), patch("db.export_table_json"), \
         patch("db.import_csv_to_table"), patch("db.import_json_to_table"), \
         patch("analysis.show_top_clients"), \
         patch("analysis.show_orders_over_time"), \
         patch("analysis.show_client_graph"):
        import gui
        return gui.App()

def test_add_client_calls_db(app):
    with patch("db.add_client") as mock_add:
        app.client_name.get = MagicMock(return_value="Test Name")
        app.email.get = MagicMock(return_value="test@example.com")
        app.phone.get = MagicMock(return_value="555")
        app.shipping_address.get = MagicMock(return_value="Street 1")

        app.add_client()
        mock_add.assert_called_once_with("Test Name", "test@example.com", "555", "Street 1")

def test_add_product_valid_price(app):
    with patch("db.add_product") as mock_add:
        app.product_name.get = MagicMock(return_value="Product X")
        app.sku.get = MagicMock(return_value="skuX")
        app.product_price.get = MagicMock(return_value="123.45")

        app.add_product()
        mock_add.assert_called_once_with("Product X", "skuX", 123.45)

def test_add_product_invalid_price(app):
    with patch("tkinter.messagebox.showerror") as mock_err:
        app.product_name.get = MagicMock(return_value="Bad Product")
        app.sku.get = MagicMock(return_value="skuBad")
        app.product_price.get = MagicMock(return_value="abc")  # не число
        app.add_product()
        mock_err.assert_called_once()

def test_add_order_calls_db(app):
    with patch("db.add_order") as mock_add:
        app.client_combo.get = MagicMock(return_value="Client1")
        app.product_combo.get = MagicMock(return_value="Product1")
        app.qty_entry.get = MagicMock(return_value="2")
        app.status_entry.get = MagicMock(return_value="новый")
        app.add_order()
        args, _ = mock_add.call_args
        assert args[0] == 1  # client_id
        assert args[1] == 2  # product_id
        assert args[2] == 2  # qty

def test_filter_orders_by_client(app):
    app.filter_client.get = MagicMock(return_value="Client1")
    app.filter_date.get = MagicMock(return_value="")
    app.orders_list.delete = MagicMock()
    app.orders_list.insert = MagicMock()
    app.filter_orders()
    app.orders_list.insert.assert_called_once()

def test_filter_orders_by_date(app):
    app.filter_client.get = MagicMock(return_value="")
    app.filter_date.get = MagicMock(return_value="2025-08-01")
    app.orders_list.delete = MagicMock()
    app.orders_list.insert = MagicMock()
    app.filter_orders()
    app.orders_list.insert.assert_called_once()

def test_export_data_csv(app):
    with patch("db.export_table_csv") as mock_export:
        app.export_data("clients", "csv")
        mock_export.assert_called_once()

def test_export_data_json(app):
    with patch("db.export_table_json") as mock_export:
        app.export_data("products", "json")
        mock_export.assert_called_once()

def test_import_data_csv(app):
    with patch("db.import_csv_to_table") as mock_import:
        app.import_data("clients", "csv")
        mock_import.assert_called_once()

def test_import_data_json(app):
    with patch("db.import_json_to_table") as mock_import:
        app.import_data("orders", "json")
        mock_import.assert_called_once()

def test_refresh_order_combos(app):
    app.client_combo = {}
    app.product_combo = {}
    app.filter_client = {}
    app.refresh_order_combos()
    assert "values" in app.client_combo
    assert "values" in app.product_combo
    assert "values" in app.filter_client
