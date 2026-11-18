from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_safe

from .forms import HomePayForm


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
