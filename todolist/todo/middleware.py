from django.utils.deprecation import MiddlewareMixin
from core.helpers import decode_jwt
from django.http import JsonResponse
from rest_framework import status
from django.contrib.auth.models import User


class AuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.path.startswith('/api/todos'):
            auth_header = request.headers.get('Authorization')
            if not auth_header:
                return JsonResponse({'error': True, 'message': 'Authoization header not available'}, status=status.HTTP_401_UNAUTHORIZED)
            token = auth_header.split(' ')[1]
            is_token_decoded, data = decode_jwt(token)
            if is_token_decoded:
                request.custom_user = User.objects.get(id=data)
            else:
                return JsonResponse({'error': True, 'message': data}, status=status.HTTP_401_UNAUTHORIZED)
