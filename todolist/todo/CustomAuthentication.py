from rest_framework.authentication import BasicAuthentication
from rest_framework.exceptions import AuthenticationFailed
from core.helpers import decode_jwt
from core.models import CustomUser, RoleChoices


class IsLoggedIn(BasicAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            raise AuthenticationFailed('Authoization header not available')
        token = auth_header.split(' ')[1]
        if not token:
            raise AuthenticationFailed('Authorization token not found')
        is_token_decoded, user_or_error = decode_jwt(token)
        if not is_token_decoded:
            raise AuthenticationFailed(user_or_error)
        return (user_or_error, None)


class CanCreateTodo(IsLoggedIn):
    def authenticate(self, request):
        result = super().authenticate(request)
        if result is None:
            return None

        user, _ = result
        if user.is_banned:
            raise AuthenticationFailed(
                'You are no longer allowed to create a Todo')
        return (user, None)


class IsAdminUser(IsLoggedIn):
    def authenticate(self, request):
        result = super().authenticate(request)

        if result is None:
            return None

        user, _ = result
        if user.role != RoleChoices.ADMIN:
            raise AuthenticationFailed(
                'Only admin is allowed to access this route')
        return (user, None)
