#!/usr/bin/env bash
# exit on error

# Обновление pip
pip install --upgrade pip

# Установка пакетов из requirements.txt
pip install -r requirements.txt

# Инициализация базы данных
flask db init

# Создание миграционного скрипта
flask db migrate

# Применение миграционного скрипта
flask db upgrade