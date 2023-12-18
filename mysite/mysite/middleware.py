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

        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        response_data = {'success': False, 'errorMessage': str(exception)}
        status = 400
        # залогировать
        return self._response(response_data, status=status)


    @staticmethod
    def _response(data, *, status):
        return JsonResponse(
            data,
            status=status,
            safe=not isinstance(data, list),
            json_dumps_params={'ensure_ascii': False, 'indent': 2}
        )
