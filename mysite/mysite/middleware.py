from django.http import JsonResponse

from logs.logger import logger
from mysite.settings import DEBUG


class YourMiddlewareClass:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        logger.info(f'Вызвано {request}')
        response = self.get_response(request)
        return response
    @staticmethod
    def process_view(request, view_func, view_args, view_kwargs):
        """ Вызывается непосредственно перед тем, как Django вызывает представление """
        if hasattr(request, 'user') and request.user.is_authenticated:
            backend_name = request.session.get('_auth_user_backend')
            if backend_name:
                logger.info(f'Использован бэкенд аутентификации: {backend_name}')

    def process_exception(self, request, exception)-> JsonResponse:
        """ стандартная функция обработки исключений """
        if not DEBUG:
            response_data = {'success': False, 'errorMessage': str(exception)}
            status = 400
            logger.warning(f'Исключение обрабатываемое в Мидлвеар, {response_data["errorMessage"]}')
            return self._response(response_data, status=status)

    @staticmethod
    def _response(data:str, *, status:int) -> JsonResponse:
        """ Формирование Json ответа """
        return JsonResponse(
            data,
            status=status,
            safe=not isinstance(data, list),
            json_dumps_params={'ensure_ascii': False, 'indent': 2},)
