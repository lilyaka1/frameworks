import json
from io import BytesIO
from zipfile import ZIP_DEFLATED, ZipFile

from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.views.decorators.http import require_GET, require_POST

from .models import Api, ApiRequest, Integration, Service, User


def _integration_data():
    return [
        {
            "id": item.id,
            "service": item.service.name,
            "api_url": item.api_url,
            "key_configured": item.key_configured,
        }
        for item in Integration.objects.select_related("service")
    ]


def dashboard(request):
    context = {
        "services": Service.objects.prefetch_related("apis__keys"),
        "requests": ApiRequest.objects.select_related("api", "user").order_by("-created_at")[:20],
        "users": User.objects.order_by("username"),
        "integrations": Integration.objects.select_related("service"),
    }
    return render(request, "dashboard.html", context)


@require_GET
@cache_page(30)
def api_integrations(request):
    return JsonResponse({"integrations": _integration_data()})


@require_POST
@login_required
def api_requests(request):
    try:
        payload = json.loads(request.body)
        api = Api.objects.get(pk=payload["api_id"])
        domain_user = User.objects.get(pk=payload["user_id"])
        status_code = int(payload["status_code"])
        duration_ms = float(payload.get("duration_ms", 0))
    except (ValueError, KeyError, TypeError, json.JSONDecodeError, Api.DoesNotExist, User.DoesNotExist):
        return JsonResponse({"error": "Некорректные данные запроса"}, status=400)

    if not 100 <= status_code <= 599 or duration_ms < 0:
        return JsonResponse({"error": "Недопустимый статус или время ответа"}, status=400)

    item = ApiRequest.objects.create(
        api=api,
        user=domain_user,
        integration=api.service.integrations.first(),
        endpoint=api.endpoint,
        method=api.method,
        status_code=status_code,
        duration_ms=duration_ms,
    )
    cache.clear()
    return JsonResponse({"id": item.id, "successful": item.successful}, status=201)


@require_GET
def health(request):
    return JsonResponse({"status": "ok"})


def export_data(request):
    archive = BytesIO()
    with ZipFile(archive, "w", ZIP_DEFLATED) as zip_file:
        zip_file.writestr(
            "integrations.json",
            json.dumps(_integration_data(), ensure_ascii=False, indent=2) + "\n",
        )
    response = HttpResponse(archive.getvalue(), content_type="application/zip")
    response["Content-Disposition"] = 'attachment; filename="api_tracker_export.zip"'
    return response
