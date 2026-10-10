"""Application operations for integrations and request statistics."""

from django.db.models import Avg, Count, Q

from .models import ApiRequest, Integration, Service


def add_integration(name, api_url, key_configured=False):
    service, _ = Service.objects.get_or_create(name=name.strip(), defaults={"url": api_url})
    return Integration.objects.create(
        service=service,
        api_url=api_url.strip().rstrip("/"),
        key_configured=key_configured,
    )


def find_integrations(query=""):
    query = query.strip()
    if not query:
        return Integration.objects.all()
    return Integration.objects.filter(
        Q(service__name__icontains=query) | Q(api_url__icontains=query)
    )


def sort_integrations(integrations=None):
    queryset = integrations if integrations is not None else Integration.objects.all()
    return queryset.order_by("service__name", "api_url")


def get_request_statistics(integration_id=None):
    requests = ApiRequest.objects.filter(integration_id=integration_id) if integration_id else ApiRequest.objects.all()
    total = requests.count()
    successful = requests.filter(status_code__gte=200, status_code__lt=300).count()
    average = requests.aggregate(value=Avg("duration_ms"))["value"] or 0.0
    return {
        "total": total,
        "successful": successful,
        "failed": total - successful,
        "success_rate": successful / total * 100 if total else 0.0,
        "average_duration_ms": average,
    }


def serialize_integrations():
    return [
        {
            "id": item.id,
            "name": item.service.name,
            "api_url": item.api_url,
            "key_configured": item.key_configured,
        }
        for item in Integration.objects.select_related("service")
    ]


def serialize_requests():
    return [
        {
            "id": item.id,
            "integration_id": item.integration_id,
            "method": item.method,
            "endpoint": item.endpoint,
            "http_status": item.status_code,
            "duration_ms": item.duration_ms,
            "requested_at": item.created_at.isoformat(),
        }
        for item in ApiRequest.objects.filter(integration__isnull=False).order_by("id")
    ]