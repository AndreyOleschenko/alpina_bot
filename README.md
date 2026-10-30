Содержание
Технологический стек

Архитектура и CI/CD

Локальный запуск

Развертывание на VPS (Production)

Переменные окружения (.env)

Технологический стек
Backend: Python 3.12, Django 4.2, Django REST Framework

Интеграции: VK API (LongPoll), Yandex Cloud ML SDK (YandexGPT)

База данных: SQLite (для простоты развертывания)

Контейнеризация: Docker, Docker Compose

Веб-сервер: Gunicorn (WSGI), Nginx (Reverse Proxy)

CI/CD: GitHub Actions, GitHub Container Registry (GHCR)

Архитектура и CI/CD
Проект использует пайплайн автоматического развертывания:

При пуше в ветку main запускается GitHub Actions.

Собирается Docker-образ приложения.

Образ публикуется в GitHub Container Registry (ghcr.io).

Actions подключается к VPS по SSH, скачивает новый образ, перезапускает контейнер и применяет изменения.

Локальный запуск
Для запуска проекта на локальной машине выполните следующие шаги:

1. Клонирование и настройка окружения
bash
git clone https://github.com/AndreyOleschenko/alpina_bot.git
cd alpina_bot/alpina_bot_constructor

# Создание и активация виртуального окружения
python -m venv venv
source venv/bin/activate  # Для Windows: venv\Scripts\activate

# Установка зависимостей
pip install -r requirements.txt
2. Настройка переменных окружения
Создайте файл .env в корне проекта (alpina_bot_constructor/) и заполните его по шаблону (см. раздел Переменные окружения).

3. Инициализация базы данных и запуск
bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
Приложение будет доступно по адресу: http://127.0.0.1:8000/

4. Запуск VK-бота
Бот запускается в отдельном процессе (терминале):

bash
python manage.py run_vk_bot
Развертывание на VPS (Production)
В репозитории настроен автоматический деплой. Однако для первоначальной настройки сервера (Ubuntu/Debian) необходимо выполнить следующие шаги:

1. Установка Docker
bash
sudo apt update
sudo apt install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
2. Подготовка директории
bash
sudo mkdir -p /opt/alpina_bot
cd /opt/alpina_bot
# Здесь должны лежать docker-compose.prod.yml, .env и db.sqlite3
3. Настройка Nginx и портов
Установите Nginx для работы в качестве Reverse Proxy (проксирует трафик с 80 порта на 8000, где работает Gunicorn):

bash
sudo apt install nginx -y
sudo ufw allow 80/tcp
sudo ufw allow 8000/tcp
4. Настройка секретов GitHub (Settings -> Secrets and variables -> Actions)
Для работы пайплайна добавьте три секрета:

VPS_HOST — IP-адрес вашего сервера (например, 155.212.142.233).

VPS_USER — имя пользователя для SSH (например, root).

VPS_SSH_KEY — приватный SSH-ключ для доступа к серверу.

Переменные окружения (.env)
Для работы проекта (как локально, так и на сервере) требуется файл .env со следующими ключами:

env
# Django секретный ключ (сгенерируйте новый для продакшена)
DJANGO_SECRET_KEY=your_super_secret_django_key

# Yandex Cloud (для работы YandexGPT)
YC_API_KEY=ваш_api_ключ_Yandex_Cloud
YC_FOLDER_ID=ваш_id_каталога

# ВКонтакте
VK_GROUP_TOKEN=ваш_токен_группы_ВК

Автор: Andrey Oleshchenko
