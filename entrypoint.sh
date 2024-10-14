#!/bin/bash

# Executa as migrações
python manage.py makemigrations
python manage.py migrate

# Inicia o servidor Django
exec python manage.py runserver 0.0.0.0:8000