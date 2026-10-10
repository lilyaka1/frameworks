from django.contrib import admin

from .models import Api, ApiKey, ApiRequest, Integration, Service, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "role")
    search_fields = ("username", "email")


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "url", "description")
    search_fields = ("name", "url")


@admin.register(Integration)
class IntegrationAdmin(admin.ModelAdmin):
    list_display = ("service", "api_url", "key_status")
    list_filter = ("key_configured",)
    search_fields = ("service__name", "api_url")


@admin.register(Api)
class ApiAdmin(admin.ModelAdmin):
    list_display = ("name", "service", "method", "version", "endpoint")
    list_filter = ("method", "version")
    search_fields = ("name", "endpoint", "service__name")


@admin.register(ApiKey)
class ApiKeyAdmin(admin.ModelAdmin):
    list_display = ("label", "api", "masked_value", "active", "expires_at")
    list_filter = ("active",)
    search_fields = ("label", "api__name")

    @admin.display(description="Ключ")
    def masked_value(self, obj):
        return obj.masked_value


@admin.register(ApiRequest)
class ApiRequestAdmin(admin.ModelAdmin):
    list_display = (
        "method",
        "endpoint",
        "status_code",
        "integration",
        "user",
        "duration_ms",
        "created_at",
    )
    list_filter = ("method", "status_code")
    search_fields = ("endpoint", "integration__service__name", "user__username")