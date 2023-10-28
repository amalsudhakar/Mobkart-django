from django.shortcuts import render
from Store.models import Product
from django.conf import settings
from django.http import FileResponse, HttpRequest, HttpResponse
from django.views.decorators.cache import cache_control
from django.views.decorators.http import require_GET


def home(request):
    products = Product.objects.all().filter(is_available=True)

    context = {
        'products':products,
    }
    return render(request, 'home.html',context)


@require_GET
@cache_control(max_age=60 * 60 * 24, immutable=True, public=True)  # one day
def favicon(request: HttpRequest) -> HttpResponse:
    file = (settings.BASE_DIR / "static/images" / "favicon.ico").open("rb")
    return FileResponse(file)