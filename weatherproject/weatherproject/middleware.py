from django.http import HttpResponse


class ExceptionMiddleware:
    def __init__(self, get_response):
        self._get_response = get_response

    def __call__(self, request):
        response = self._get_response(request)
        return response

    def process_exception(self, request, exception):
        """Base handler for exceptions in views"""
        print("Exception occurred while running.")
        print(f"Exception: {exception}")
        return HttpResponse({"message": "Something went wrong"}, status=500)
