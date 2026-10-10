from django.shortcuts import render
from .models import Service, ApiRequest

def dashboard(request):
    return render(request, "dashboard.html", {"services": Service.objects.prefetch_related("apis"), "requests": ApiRequest.objects.order_by("-created_at")[:20]})
