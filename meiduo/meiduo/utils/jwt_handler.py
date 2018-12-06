from rest_framework_jwt.utils import jwt_response_payload_handler
from rest_framework_jwt.utils import jwt_payload_handler


def jwt_response_handler(token, user=None, request=None):
    return {
        'token': token,
        'username': user.username,
        'user_id': user.id
    }


def jwt_payload_handler2(user):
    payload = jwt_payload_handler(user)
    if 'email' in payload:
        del payload['email']
    payload['mobile'] = user.mobile
    return payload