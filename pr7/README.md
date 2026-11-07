# Практические занятия №6–8

## Запуск локально

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Проверки доступности: `GET /health/`. REST-ресурс интеграций: `GET /api/integrations/`.
Создание записи о запросе: `POST /api/requests/`; endpoint доступен только
аутентифицированному пользователю Django Admin и принимает JSON с `api_id`,
`user_id`, `status_code` и необязательным `duration_ms`.

## Деплой

Скопируйте `.env.example` в `.env`, задайте случайный `DJANGO_SECRET_KEY`, затем:

```bash
docker compose up --build -d
docker compose ps
curl http://localhost:8000/health/
```

Контейнер запускает Gunicorn, автоматически перезапускается и имеет healthcheck.
Перед публикацией за reverse proxy следует включить HTTPS, ограничить
`DJANGO_ALLOWED_HOSTS`, хранить секреты вне репозитория и настроить резервное
копирование базы данных.
