from rest_framework_jwt.utils import jwt_response_payload_handler


def jwt_response_handler(token, user=None, request=None):
    return {
        'token': token,
        'username': user.username,
        'user_id': user.id
    }
