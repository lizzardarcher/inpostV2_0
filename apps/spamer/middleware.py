from django.http import HttpResponseForbidden


class BlockDomainMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        text = """
        <h1>Доступ запрещен!</h1> 
        <p>Передайте владельцу, чтобы отвязали все старые ip адреса от</p>
        <p>домена vsevtai.ru!!!</p>
        """
        # Проверяем, совпадает ли хост запроса с запрещенным доменом
        if 'vsevtai.ru' in request.META['HTTP_HOST']:
            return HttpResponseForbidden(text)

        response = self.get_response(request)
        return response
