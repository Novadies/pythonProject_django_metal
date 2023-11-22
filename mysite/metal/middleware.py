from icecream import ic

ic.configureOutput(includeContext=True)  # указание строки и места выполнения


class YourMiddlewareClass:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ic(request.path)
        response = self.get_response(request)

        print("это выполнится в конце ")

        return response
