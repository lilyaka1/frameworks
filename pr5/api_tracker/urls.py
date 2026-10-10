from django.urls import path
from integrations.views import dashboard

urlpatterns = [path("", dashboard, name="dashboard")]
