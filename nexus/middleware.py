class XForwardedHostMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if 'X-Forwarded-Host' in request.headers:
            request.is_secure = lambda: True
        return self.get_response(request)
