from datetime import date, timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from integrations.models import Api, ApiKey, ApiRequest, Integration, Service, User


class Command(BaseCommand):
    help = "Заполняет базу демонстрационными данными для ПР5."

    def handle(self, *args, **options):
        users = self._create_users()
        catalog = self._create_services_and_apis()
        integrations = self._create_integrations(catalog)
        requests = self._create_requests(users, catalog, integrations)

        self.stdout.write(self.style.SUCCESS(
            "База заполнена: "
            f"пользователей — {User.objects.count()}, "
            f"сервисов — {Service.objects.count()}, "
            f"API — {Api.objects.count()}, "
            f"ключей — {ApiKey.objects.count()}, "
            f"интеграций — {Integration.objects.count()}, "
            f"запросов — {ApiRequest.objects.count()}."
        ))

    def _create_users(self):
        data = [
            ("admin", "admin@example.com", "administrator"),
            ("analyst", "analyst@example.com", "analyst"),
            ("developer", "developer@example.com", "developer"),
        ]
        result = {}
        for username, email, role in data:
            user, _ = User.objects.update_or_create(
                username=username,
                defaults={"email": email, "role": role},
            )
            result[username] = user
        return result

    def _create_services_and_apis(self):
        data = {
            "Погода": {
                "url": "https://weather.example.com",
                "description": "Прогноз погоды и метеоданные.",
                "apis": [("Weather API", "/forecast", "GET", "v1", "Основной")],
            },
            "Курсы валют": {
                "url": "https://currency.example.com",
                "description": "Актуальные курсы валют.",
                "apis": [("Currency API", "/rates", "GET", "v2", "Основной")],
            },
            "Доставка": {
                "url": "https://delivery.example.com",
                "description": "Расчет доставки и отслеживание отправлений.",
                "apis": [("Delivery API", "/shipments", "POST", "v1", "Боевой")],
            },
        }
        result = {}
        for name, item in data.items():
            service, _ = Service.objects.update_or_create(
                name=name,
                defaults={"url": item["url"], "description": item["description"]},
            )
            api_data = item["apis"][0]
            api, _ = Api.objects.update_or_create(
                service=service,
                name=api_data[0],
                defaults={
                    "endpoint": api_data[1],
                    "method": api_data[2],
                    "version": api_data[3],
                },
            )
            ApiKey.objects.update_or_create(
                api=api,
                label=api_data[4],
                defaults={
                    "value": f"demo_{name.lower().replace(' ', '_')}_key",
                    "active": name != "Курсы валют",
                    "expires_at": date.today() + timedelta(days=365),
                },
            )
            result[name] = {"service": service, "api": api}
        return result

    def _create_integrations(self, catalog):
        configured = {"Погода": True, "Курсы валют": False, "Доставка": True}
        result = {}
        for name, item in catalog.items():
            integration, _ = Integration.objects.update_or_create(
                service=item["service"],
                api_url=f"{item['service'].url}/api/{item['api'].version}",
                defaults={"key_configured": configured[name]},
            )
            result[name] = integration
        return result

    def _create_requests(self, users, catalog, integrations):
        data = [
            ("Погода", "admin", "GET", "/forecast/today", 200, 142.5),
            ("Погода", "developer", "GET", "/forecast/week", 503, 812.0),
            ("Курсы валют", "analyst", "GET", "/rates/latest", 200, 97.3),
            ("Доставка", "developer", "POST", "/shipments/quote", 201, 234.8),
            ("Доставка", "admin", "POST", "/shipments/track", 404, 188.2),
        ]
        for service_name, username, method, endpoint, status, duration in data:
            integration = integrations[service_name]
            api = catalog[service_name]["api"]
            request, created = ApiRequest.objects.get_or_create(
                integration=integration,
                user=users[username],
                method=method,
                endpoint=endpoint,
                defaults={
                    "api": api,
                    "status_code": status,
                    "duration_ms": duration,
                },
            )
            if not created:
                request.api = api
                request.status_code = status
                request.duration_ms = duration
                request.save(update_fields=["api", "status_code", "duration_ms"])
        return ApiRequest.objects.all()