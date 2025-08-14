import unittest
from datetime import datetime
from models import Person, Client, Product, Order


class TestPerson(unittest.TestCase):
    def test_display(self):
        p = Person("Alice", "alice@example.com", "+123456789", "123 Street")
        self.assertEqual(
            p.display(),
            "Alice - alice@example.com - +123456789 123 Street"
        )


class TestClient(unittest.TestCase):
    def test_client_initialization_valid(self):
        c = Client(1, "Bob", "bob@example.com", "+987654321", "Lenina 10, kv.5")
        self.assertEqual(c.client_id, 1)
        self.assertEqual(c.name, "Bob")
        self.assertEqual(c.email, "bob@example.com")
        self.assertEqual(c.phone, "+987654321")
        self.assertEqual(c.shipping_address, "Lenina 10, kv.5")
        self.assertTrue(isinstance(c, Person))

    def test_client_invalid_email(self):
        with self.assertRaises(ValueError) as cm:
            Client(1, "Bob", "wrong.com", "+987654321", "Lenina 10")
        self.assertIn("Некорректный email", str(cm.exception))

    def test_client_invalid_phone(self):
        with self.assertRaises(ValueError) as cm:
            Client(1, "Bob", "bob@example.com", "abc123", "Lenina 10")
        self.assertIn("Некорректный телефон", str(cm.exception))

    def test_client_invalid_address(self):
        with self.assertRaises(ValueError) as cm:
            Client(1, "Bob", "bob@example.com", "+987654321", "")
        self.assertIn("Некорректный адрес", str(cm.exception))


class TestProduct(unittest.TestCase):
    def test_product_initialization_valid(self):
        p = Product(10, "Laptop", "SKU123", 1500.0)
        self.assertEqual(p.product_id, 10)
        self.assertEqual(p.name, "Laptop")
        self.assertEqual(p.sku, "SKU123")
        self.assertEqual(p.price, 1500.0)

    def test_product_negative_price(self):
        with self.assertRaises(ValueError) as cm:
            Product(11, "Phone", "SKU456", -100.0)
        self.assertIn("Цена не может быть отрицательной", str(cm.exception))


class TestOrder(unittest.TestCase):
    def test_order_with_defaults(self):
        o = Order(100, 1, 10, 2)
        self.assertEqual(o.order_id, 100)
        self.assertEqual(o.client_id, 1)
        self.assertEqual(o.product_id, 10)
        self.assertEqual(o.quantity, 2)
        self.assertTrue(o.created_at.startswith(datetime.now().strftime('%Y-%m-%d')))
        self.assertEqual(o.status, "в ожидании")

    def test_order_with_custom_values(self):
        custom_date = "2025-01-01 12:00:00"
        o = Order(101, 2, 11, 5, created_at=custom_date, status="доставлен")
        self.assertEqual(o.created_at, custom_date)
        self.assertEqual(o.status, "доставлен")

    def test_order_negative_quantity(self):
        with self.assertRaises(ValueError) as cm:
            Order(103, 3, 12, 0)
        self.assertIn("Количество должно быть положительным", str(cm.exception))

    def test_total_price(self):
        o = Order(102, 3, 12, 3)
        self.assertEqual(o.total_price(100.0), 300.0)
        self.assertEqual(o.total_price(0), 0)
        self.assertEqual(o.total_price(19.99), 3 * 19.99)


if __name__ == "__main__":
    unittest.main()
