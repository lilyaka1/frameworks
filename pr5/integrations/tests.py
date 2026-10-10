from django.test import TestCase

from .models import Api, ApiRequest, Integration, Service, User
from .services import get_request_statistics, find_integrations, sort_integrations


class IntegrationTests(TestCase):
    def setUp(self):
        self.service = Service.objects.create(name="Weather", url="https://weather.example")
        self.integration = Integration.objects.create(
            service=self.service, api_url="https://weather.example/v1", key_configured=True
        )
        self.api = Api.objects.create(
            service=self.service,
            name="Weather API",
            endpoint="/health",
        )
        self.user = User.objects.create(username="admin", email="admin@example.com")

    def test_search_and_sort_integrations(self):
        other = Service.objects.create(name="Currency", url="https://currency.example")
        Integration.objects.create(service=other, api_url="https://currency.example/v1")
        self.assertEqual(find_integrations("WEATHER").count(), 1)
        self.assertEqual(list(sort_integrations().values_list("service__name", flat=True)), ["Currency", "Weather"])

    def test_request_statistics(self):
        ApiRequest.objects.create(api=self.api, integration=self.integration, user=self.user, method="GET", endpoint="/ok", status_code=200, duration_ms=20)
        ApiRequest.objects.create(api=self.api, integration=self.integration, user=self.user, method="GET", endpoint="/fail", status_code=500, duration_ms=40)
        stats = get_request_statistics(self.integration.id)
        self.assertEqual(stats["total"], 2)
        self.assertEqual(stats["successful"], 1)
        self.assertEqual(stats["success_rate"], 50.0)
        self.assertEqual(stats["average_duration_ms"], 30.0)