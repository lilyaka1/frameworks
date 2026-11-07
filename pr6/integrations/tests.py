import json

from django.contrib.auth.models import User as DjangoUser
from django.test import TestCase

from .models import Api, Integration, Service, User


class IntegrationApiTests(TestCase):
    def setUp(self):
        self.service = Service.objects.create(name="Weather", url="https://weather.example")
        Integration.objects.create(service=self.service, api_url="https://weather.example/v1")
        self.api = Api.objects.create(service=self.service, name="Weather API", endpoint="/health")
        self.user = User.objects.create(username="operator", email="operator@example.com")

    def test_public_api_is_cached_shape(self):
        response = self.client.get("/api/integrations/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["integrations"][0]["service"], "Weather")

    def test_request_api_requires_authentication(self):
        response = self.client.post("/api/requests/", data="{}", content_type="application/json")
        self.assertEqual(response.status_code, 302)

    def test_authenticated_request_validates_and_creates_record(self):
        DjangoUser.objects.create_user(username="admin", password="safe-password")
        self.client.login(username="admin", password="safe-password")
        response = self.client.post(
            "/api/requests/",
            data=json.dumps({"api_id": self.api.id, "user_id": self.user.id, "status_code": 200}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)
