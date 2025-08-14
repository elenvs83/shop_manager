from db import init_db, add_client, add_product, add_order
import random
from datetime import date, timedelta, datetime

init_db()

clients = [
    ("Иван Иванов", "ivan@example.com", "89012345678", "г. Москва, ул. Пушкина, д. 1, кв. 1"),
    ("Пётр Петров", "petr@example.com", "89012345679", "г. Санкт-Петербург, ул. Ленина, д. 2, кв. 2"),
    ("Мария Смирнова", "maria@example.com", "89012345680", "г. Казань, ул. Сибирская, д. 3, кв. 3"),
    ("Анна Кузнецова", "anna@example.com", "89012345681", "г. Екатеринбург, ул. Уральская, д. 4, кв. 4"),
    ("Олег Сидоров", "oleg@example.com", "89012345682", "г. Новосибирск, ул. Ленина, д. 5, кв. 5")
]
products = [
    ("Футболка", "1662517302", 10.5),
    ("Кружка", "1644932623", 7.0),
    ("Блокнот", "11747084298", 3.2),
    ("Рюкзак", "17420070", 25.0),
    ("Наклейки", "1262780561", 1.0)
]

cids = [add_client(n, c, p, a) for n, c, p, a in clients]
pids = [add_product(n, c, p) for n, c, p in products]

for _ in range(30):
    cid = random.choice(cids)
    pid = random.choice(pids)
    qty = random.randint(1, 5)
    random_days = random.randint(0, 9)
    random_hours = random.randint(0, 23)
    random_minutes = random.randint(0, 59)
    random_seconds = random.randint(0, 59)

    d = datetime.now() - timedelta(
        days=random_days,
        hours=random_hours,
        minutes=random_minutes,
        seconds=random_seconds
    )
    add_order(cid, pid, qty, d.strftime('%Y-%m-%d %H:%M:%S'), "в ожидании")

print("Тестовые данные добавлены.")
