#!/usr/bin/env bash
set -e
python -m pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate
python manage.py showmigrations

if [ -f "seed_demo_data.py" ]; then
    echo "Запуск скрипта наполнения базы данных..."
    python seed_demo_data.py
fi
