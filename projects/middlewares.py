from django.http import HttpResponseForbidden

class PermissionDeniedMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if response.status_code == 403:
            return HttpResponseForbidden('Данная функция вам недоступна')
        return response
