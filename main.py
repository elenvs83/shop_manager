"""
Точка входа: инициализация БД и запуск GUI.
"""
from db import init_db
from gui import App

if __name__ == "__main__":
    init_db()
    app = App()
    app.mainloop()
