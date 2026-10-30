# Dockerfile
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Установка системных зависимостей (если нужны для сборки пакетов)
RUN apt-get update && apt-get install -y --no-install-recommends gcc && rm -rf /var/lib/apt/lists/*

# Копирование и установка Python-зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование кода проекта
COPY . .

# Сбор статики (для админки)
RUN python manage.py collectstatic --noinput

# Открытие порта
EXPOSE 8000

# Запуск через Gunicorn
CMD ["gunicorn", "bot_constructor.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]