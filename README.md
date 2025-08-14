# Установка и запуск

## Перейти в каталог shop_manager

cd shop_manager

## Создать виртуальное окружение Python в папке venv - Windows

python -m venv venv

## Создать виртуальное окружение Python в папке venv - Linux/Mac

python3 -m venv venv

## Активировать виртуальное окружение Python, созданное в папке venv - Windows

venv\Scripts\activate

## Активировать виртуальное окружение Python, созданное в папке venv - Linux/Mac

source venv/bin/activate

## Загрузить и установить библиотеки в виртуальное окружение

pip install -r requirements.txt

## Наполнить db

python sample_data.py

## Запустить

python main.py

## Запустить тесты - Linux/Mac

python3 -m unittest discover -s tests -v

## Запустить тесты - Windows

python -m unittest discover -s tests -v