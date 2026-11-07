from django.contrib import admin
from django.urls import path
from integrations.views import api_integrations, api_requests, dashboard, export_data, health

urlpatterns = [
    path("", dashboard, name="dashboard"),
    path("export/", export_data, name="export_data"),
    path("api/integrations/", api_integrations, name="api_integrations"),
    path("api/requests/", api_requests, name="api_requests"),
    path("health/", health, name="health"),
    path("admin/", admin.site.urls),
]
