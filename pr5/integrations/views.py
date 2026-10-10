from django.shortcuts import render
from .models import ApiRequest, Service, User
from .services import get_request_statistics, find_integrations, sort_integrations


def dashboard(request):
    query = request.GET.get("q", "")
    integrations = sort_integrations(find_integrations(query))
    context = {
        "services": Service.objects.prefetch_related("apis__keys"),
        "requests": ApiRequest.objects.select_related("api", "user").order_by("-created_at")[:20],
        "users": User.objects.order_by("username"),
        "integrations": integrations,
        "query": query,
        "statistics": get_request_statistics(),
    }
    return render(request, "dashboard.html", context)
