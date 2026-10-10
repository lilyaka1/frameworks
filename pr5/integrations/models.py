from django.db import models

class Service(models.Model):
    name = models.CharField(max_length=120)
    url = models.URLField()
    description = models.TextField(blank=True)
    def __str__(self): return self.name

class Api(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="apis")
    name = models.CharField(max_length=120)
    endpoint = models.CharField(max_length=255)
    version = models.CharField(max_length=30, default="v1")

class ApiKey(models.Model):
    api = models.ForeignKey(Api, on_delete=models.CASCADE, related_name="keys")
    label = models.CharField(max_length=120)
    value = models.CharField(max_length=255)
    expires_at = models.DateField(null=True, blank=True)

class ApiRequest(models.Model):
    api = models.ForeignKey(Api, on_delete=models.CASCADE, related_name="requests")
    method = models.CharField(max_length=10)
    status_code = models.PositiveSmallIntegerField()
    user = models.CharField(max_length=120)
    created_at = models.DateTimeField(auto_now_add=True)
