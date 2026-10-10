from django.db import models


class User(models.Model):
    username = models.CharField(max_length=120, unique=True)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=30, default="viewer")

    def __str__(self):
        return self.username


class Service(models.Model):
    name = models.CharField(max_length=120)
    url = models.URLField()
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Integration(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="integrations")
    api_url = models.URLField()
    key_configured = models.BooleanField(default=False)

    class Meta:
        ordering = ["service__name"]
        constraints = [
            models.UniqueConstraint(fields=["service", "api_url"], name="unique_service_api_url")
        ]

    @property
    def key_status(self):
        return "Ключ доступа настроен" if self.key_configured else "Ключ доступа не настроен"

    def __str__(self):
        return f"{self.service.name} | {self.api_url}"


class Api(models.Model):
    HTTP_METHODS = [(method, method) for method in ("GET", "POST", "PUT", "PATCH", "DELETE")]
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="apis")
    name = models.CharField(max_length=120)
    endpoint = models.CharField(max_length=255)
    method = models.CharField(max_length=10, choices=HTTP_METHODS, default="GET")
    version = models.CharField(max_length=30, default="v1")

    def __str__(self):
        return f"{self.name} ({self.version})"


class ApiKey(models.Model):
    api = models.ForeignKey(Api, on_delete=models.CASCADE, related_name="keys")
    label = models.CharField(max_length=120)
    value = models.CharField(max_length=255)
    active = models.BooleanField(default=True)
    expires_at = models.DateField(null=True, blank=True)

    @property
    def masked_value(self):
        return f"{self.value[:4]}***" if self.value else "***"


class ApiRequest(models.Model):
    api = models.ForeignKey(Api, on_delete=models.CASCADE, related_name="requests")
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="requests")
    integration = models.ForeignKey(
        Integration,
        on_delete=models.CASCADE,
        related_name="api_requests",
        null=True,
        blank=True,
    )
    endpoint = models.CharField(max_length=255, blank=True)
    duration_ms = models.FloatField(default=0)
    method = models.CharField(max_length=10)
    status_code = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def successful(self):
        return 200 <= self.status_code < 300

    @property
    def status(self):
        return "Запрос выполнен успешно" if self.successful else "Запрос завершился ошибкой"
