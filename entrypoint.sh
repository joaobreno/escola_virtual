#!/bin/bash

# Espera o banco de dados estar pronto
while ! nc -z postgres_db 5432; do
  echo "Aguardando o PostgreSQL iniciar..."
  sleep 1
done

# Executa as migrações
python manage.py makemigrations
python manage.py migrate

# Inicia o servidor Django
exec python manage.py runserver 0.0.0.0:8000