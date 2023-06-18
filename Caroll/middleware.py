from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect
from django_redis import get_redis_connection


class LoginMiddleware(MiddlewareMixin):
    def process_request(self, request):
        conn = get_redis_connection()
        uid = conn.get('username')
        if not uid and request.path not in ['/login', '/register', '/send/sms']:
            return redirect("login")

