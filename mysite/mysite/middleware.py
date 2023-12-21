from django.http import JsonResponse
import logging

from mysite.settings import DEBUG

logger = logging.getLogger('metal')

class YourMiddlewareClass:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        logger.debug(f'Вызвано {request}')
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception)-> JsonResponse:
        """ стандартная функция обработки исключений """
        if not DEBUG:
            response_data = {'success': False, 'errorMessage': str(exception)}
            status = 400
            logger.warning(f'Исключение обрабатываемое в Мидлвеар, {response_data["errorMessage"]}')
            return self._response(response_data, status=status)

    @staticmethod
    def _response(data:str, *, status:int) -> JsonResponse:
        """ формирование Json ответа """
        return JsonResponse(
            data,
            status=status,
            safe=not isinstance(data, list),
            json_dumps_params={'ensure_ascii': False, 'indent': 2},)
