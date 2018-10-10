from django.http import HttpResponse
from django.views.decorators.http import require_GET


@require_GET
def test_view(request):
    return HttpResponse('This is a test view')
