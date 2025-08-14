"""
Модели данных для системы учёта интернет магазина.

Все классы содержат docstrings в формате numpydoc.
"""
from dataclasses import dataclass
from datetime import datetime
import re


def validate_email(email: str) -> bool:
    """Проверка email с помощью regex."""
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return bool(re.match(pattern, email))


def validate_phone(phone: str) -> bool:
    """Проверка телефона (простой формат: +, код, цифры)."""
    pattern = r"^\+?\d{7,15}$"
    return bool(re.match(pattern, phone))


def validate_address(address: str) -> bool:
    """Проверка адреса доставки.
    Допустим формат: улица/проспект, номер дома, опционально квартира.
    """
    pattern = r"^[\w\s\.\-\,]+$"  # допускаем буквы, цифры, пробелы, точку, запятую и дефис
    return bool(re.match(pattern, address)) and len(address.strip()) >= 5


@dataclass
class Person:
    name: str
    email: str
    phone: str
    shipping_address: str

    def display(self):
        return f"{self.name} - {self.email} - {self.phone} {self.shipping_address}"


@dataclass
class Client(Person):
    """
    Клиент интернет-магазина.

    Parameters
    ----------
    name : str
        Имя/ФИО клиента.
    email : str
        Электронная почта (валидируется regex).
    phone : str
        Телефон (валидируется regex).
    shipping_address : str
        Адрес доставки (валидируется regex).
    """
    def __init__(self, client_id: int, name: str, email: str, phone: str, shipping_address: str):
        if not validate_email(email):
            raise ValueError(f"Некорректный email: {email}")
        if not validate_phone(phone):
            raise ValueError(f"Некорректный телефон: {phone}")
        if not validate_address(shipping_address):
            raise ValueError(f"Некорректный адрес: {shipping_address}")

        super().__init__(name, email, phone, shipping_address)
        self.client_id = client_id
        self.email = email
        self.phone = phone
        self.shipping_address = shipping_address


@dataclass
class Product:
    """
    Товар каталога.
    """
    def __init__(self, product_id: int, name: str, sku: str, price: float):
        if price < 0:
            raise ValueError("Цена не может быть отрицательной")
        self.product_id = product_id
        self.name = name
        self.sku = sku
        self.price = price


class Order:
    def __init__(self, order_id: int, client_id: int, product_id: int, quantity: int, created_at: str = None, status: str = None):
        if quantity <= 0:
            raise ValueError("Количество должно быть положительным")
        self.order_id = order_id
        self.client_id = client_id
        self.product_id = product_id
        self.quantity = quantity
        self.created_at = created_at or datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.status = status or "в ожидании"

    def total_price(self, product_price: float):
        return self.quantity * product_price
