from django.contrib import admin

from .models import Api, ApiKey, ApiRequest, Integration, Service, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "role")
    search_fields = ("username", "email")


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    search_fields = ("name", "url")


@admin.register(Integration)
class IntegrationAdmin(admin.ModelAdmin):
    list_display = ("service", "api_url", "key_configured")
    list_filter = ("key_configured",)


@admin.register(Api)
class ApiAdmin(admin.ModelAdmin):
    list_display = ("name", "service", "method", "version", "endpoint")
    list_filter = ("method", "version")


@admin.register(ApiKey)
class ApiKeyAdmin(admin.ModelAdmin):
    list_display = ("label", "api", "active", "expires_at")


@admin.register(ApiRequest)
class ApiRequestAdmin(admin.ModelAdmin):
    list_display = ("method", "endpoint", "status_code", "user", "created_at")
    list_filter = ("method", "status_code")
