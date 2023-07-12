from django.shortcuts import render


class ErrorHandlerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        context = {
            'error': exception,
        }
        return render(request, 'error404.html', context)
