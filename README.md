# Система учета API-интеграций

* логин: `admin`
* пароль: `Admin12345!`
* email: `admin@example.com`

Предметная область: сервис, API, ключ, запрос, пользователь.

Практики расположены отдельно и развиваются последовательно:

- `pr1` — базовые структуры и операции с сервисами;
- `pr2` — dataclass-модели и реестр;
- `pr3` — ООП-модель предметной области;
- `pr5` — Django-проект с моделями и страницей учета;
- `pr6` — место для следующего этапа на базе Django-проекта `pr5`.

Запуск `pr5`:

```bash
cd pr5
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py runserver
```
