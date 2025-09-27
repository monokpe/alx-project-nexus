from django.http import HttpResponse

def headers_view(request):
    return HttpResponse(str(request.headers))
