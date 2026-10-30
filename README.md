# Alpina GPT Bot Constructor

API для создания ботов с GPT-сценариями и интеграцией с VK.

## Быстрый старт

```bash
git clone <repo>
cd alpina-gpt-bot-constructor
python -m venv venv
source venv/bin/activate  # или .\venv\Scripts\activate на Windows
pip install -r requirements.txt
cp .env.example .env   # и заполнить ключи
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver