from django.http import JsonResponse


class YourMiddlewareClass:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            ic(request.path)
        except Exception:
            from icecream import ic
            print('IC опять не отработал!!')
            ic(request.path)

        try:
            response = self.get_response(request)
        except Exception as e:
            response_data = {'errorMessage': str(e)} # или Exception.message ?
            response = self._response(response_data, status=400)
        return response
    @staticmethod
    def _response(data, *, status=200):
        return JsonResponse(
            data,
            status=status,
            safe=not isinstance(data, list),
            json_dumps_params={'ensure_ascii': False}
        )
