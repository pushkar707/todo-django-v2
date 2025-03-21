import jwt
import time
from core.models import CustomUser

JWT_SECRET_KEY = "ERSDDFXCDFXDFCERF"


def create_jwt(payload, expires_in):
    payload['exp'] = time.time() + expires_in
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm='HS256')


def decode_jwt(token):
    data = None
    try:
        data = jwt.decode(token, JWT_SECRET_KEY, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return False, 'Token expired'
    except jwt.InvalidSignatureError:
        return False, 'Token Invalid'
    except jwt.InvalidTokenError:
        return False, 'Token Invalid'

    user_id = data.get('user_id')
    try:
        user = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        return False, 'This account no longer exists'
    return True, user
