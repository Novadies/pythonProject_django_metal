
class YourMiddlewareClass:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            ic(request.path)
        except Exception:
            from icecream import ic
            ic(request.path)

        response = self.get_response(request)

        print("это выполнится в конце ")

        return response
