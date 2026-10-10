"""ПР2. Консольный учет сервисов, API, ключей и запросов."""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class ApiKey:
    name: str
    value: str
    expires_at: str = ""

    @property
    def masked(self):
        return self.value[:4] + "***" if len(self.value) > 4 else "***"


@dataclass
class Api:
    name: str
    base_url: str
    version: str = "v1"
    keys: list[ApiKey] = field(default_factory=list)


@dataclass
class Service:
    name: str
    description: str
    apis: list[Api] = field(default_factory=list)


@dataclass
class ApiRequest:
    method: str
    endpoint: str
    status_code: int
    user: str
    created_at: str = field(default_factory=lambda: datetime.now().isoformat(timespec="seconds"))


class IntegrationRegistry:
    def __init__(self):
        self.services: list[Service] = []
        self.requests: list[ApiRequest] = []

    def add_service(self, service: Service):
        self.services.append(service)

    def log_request(self, request: ApiRequest):
        self.requests.append(request)

    def report(self):
        return {"services": len(self.services), "apis": sum(len(s.apis) for s in self.services), "requests": len(self.requests)}


if __name__ == "__main__":
    registry = IntegrationRegistry()
    api = Api("Платежный API", "https://payments.example.com", "v1", [ApiKey("Основной", "sk_live_123456")])
    registry.add_service(Service("Платежи", "Прием платежей", [api]))
    registry.log_request(ApiRequest("GET", "/payments", 200, "admin"))
    print(registry.report())
