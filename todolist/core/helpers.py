import jwt
import time
from django.contrib.auth.models import User

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
    user = User.objects.filter(id=user_id, is_active=True).exists()
    if not user:
        return False, 'This account no longer exists'
    return True, user_id
