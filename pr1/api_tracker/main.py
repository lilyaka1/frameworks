"""ПР1. Базовая версия системы учета API-интеграций."""

services = []


def add_service(name, url, description=""):
    services.append({"name": name, "url": url, "description": description})


def show_services():
    if not services:
        print("Сервисы пока не добавлены.")
        return
    for number, service in enumerate(services, 1):
        print(f"{number}. {service['name']} — {service['url']} ({service['description']})")


if __name__ == "__main__":
    add_service("Платежи", "https://payments.example.com", "Оплата заказов")
    add_service("Погода", "https://weather.example.com", "Прогноз погоды")
    print("Система учета API-интеграций")
    show_services()
