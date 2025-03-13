from rest_framework.authentication import BasicAuthentication
from rest_framework.exceptions import AuthenticationFailed
from core.helpers import decode_jwt


class IsLoggedIn(BasicAuthentication):
    '''
    Checks for access token in Authorzation header and validates the token
    '''

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
