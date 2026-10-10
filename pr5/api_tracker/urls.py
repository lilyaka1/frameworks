from django.contrib import admin
from django.urls import path
from integrations.views import dashboard

urlpatterns = [
    path("", dashboard, name="dashboard"),
    path("admin/", admin.site.urls),
]
