"""ПР3. ООП-модели предметной области."""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class User:
    username: str
    email: str
    role: str = "viewer"


@dataclass
class ApiKey:
    label: str
    secret: str
    active: bool = True

    def masked(self):
        return f"{self.secret[:4]}***" if self.secret else "***"


@dataclass
class Api:
    name: str
    endpoint: str
    method: str = "GET"
    version: str = "v1"
    keys: list[ApiKey] = field(default_factory=list)

    def add_key(self, key: ApiKey):
        self.keys.append(key)


@dataclass
class Service:
    name: str
    url: str
    apis: list[Api] = field(default_factory=list)

    def add_api(self, api: Api):
        self.apis.append(api)


@dataclass
class ApiRequest:
    api: Api
    user: User
    status: int
    created_at: datetime = field(default_factory=datetime.now)

    @property
    def successful(self):
        return 200 <= self.status < 300


class IntegrationSystem:
    def __init__(self):
        self.services = []
        self.users = []
        self.requests = []

    def add_service(self, service):
        self.services.append(service)

    def add_user(self, user):
        self.users.append(user)

    def record_request(self, request):
        self.requests.append(request)

    def statistics(self):
        return {"services": len(self.services), "users": len(self.users), "requests": len(self.requests), "successful": sum(r.successful for r in self.requests)}
