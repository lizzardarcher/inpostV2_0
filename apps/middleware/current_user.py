import traceback
from threading import local

from django.utils.deprecation import MiddlewareMixin

_user = local()


class CurrentUserMiddleware(MiddlewareMixin):
    def process_request(self, request):
        _user.value = request.user
        _user.id = request.user.id
        # print(_user.value)
        # print(_user.id)


def get_current_user():
    try:
        return _user.value
    except AttributeError:
        return None


def get_current_user_id():
    try:
        return _user.id
    except AttributeError:
        print(traceback.fromat_exc())
        return None

