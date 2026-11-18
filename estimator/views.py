from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import (
    require_http_methods,
    require_POST,
    require_safe,
)

from .forms import HomePayForm
from .sources import COST_GUIDANCE, IMMIGRATION_GUIDANCE


@require_http_methods(["GET", "POST"])
def index(request):
    form = HomePayForm(request.POST if request.method == "POST" else None)
    gross_home_pay = None
    status = 200
    if form.is_bound:
        if form.is_valid():
            gross_home_pay = f"{form.home_pay_gbp():,.2f}"
        else:
            status = 400

    context = {
        "form": form,
        "gross_home_pay": gross_home_pay,
        "cost_guidance": COST_GUIDANCE,
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
        return JsonResponse(
            {
                "error": "Check the highlighted fields.",
                "fields": form.errors.get_json_data(),
            },
            status=400,
        )
    return JsonResponse({"gross_home_pay_gbp": str(form.home_pay_gbp())})
