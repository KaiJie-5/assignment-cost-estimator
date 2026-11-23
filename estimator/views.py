import json
from decimal import Decimal, InvalidOperation

from django.http import HttpResponseServerError, JsonResponse
from django.shortcuts import render
from django.views.decorators.http import (
    require_http_methods,
    require_POST,
    require_safe,
)

from .cost_report import cost_report
from .forms import CostEstimateForm, HomePayForm
from .sources import IMMIGRATION_GUIDANCE, UK_WORKPLACE_RELIEF


@require_http_methods(["GET", "POST"])
def index(request):
    form = CostEstimateForm(request.POST if request.method == "POST" else None)
    report = None
    status = 200
    if form.is_bound:
        if form.is_valid():
            report = cost_report(form.estimate())
        else:
            status = 400
            for field in form:
                if field.errors:
                    field.field.widget.attrs["class"] += " is-invalid"

    context = {
        "form": form,
        "report": report,
        "housing_relief_source": UK_WORKPLACE_RELIEF,
        "immigration_guidance": IMMIGRATION_GUIDANCE,
    }
    return render(request, "estimator/index.html", context, status=status)


@require_safe
def health(request):
    return JsonResponse({"status": "ok"})


@require_POST
def home_pay(request):
    form = HomePayForm(request.POST)
    if not form.is_valid():
        return _invalid_fields(form)
    return JsonResponse({"gross_home_pay_gbp": str(form.home_pay_gbp())})


@require_POST
def estimate_cost(request):
    data = request.POST
    if request.content_type == "application/json":
        try:
            data = json.loads(request.body, parse_float=Decimal, parse_constant=Decimal)
        except (ValueError, InvalidOperation, RecursionError):
            data = None
        if not isinstance(data, dict):
            return JsonResponse(
                {"error": "Send a JSON object with the estimate fields.", "fields": {}},
                status=400,
            )

    form = CostEstimateForm(data)
    if not form.is_valid():
        return _invalid_fields(form)
    return JsonResponse(cost_report(form.estimate()))


def _invalid_fields(form):
    return JsonResponse(
        {
            "error": "Check the highlighted fields.",
            "fields": form.errors.get_json_data(),
        },
        status=400,
    )


def server_error(request):
    message = "Something went wrong. Please try again."
    if request.path_info.startswith("/api/"):
        return JsonResponse({"error": message}, status=500)
    return HttpResponseServerError(message, content_type="text/plain")
