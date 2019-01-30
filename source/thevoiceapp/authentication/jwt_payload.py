from datetime import datetime, timedelta

from rest_framework_jwt.settings import api_settings

jwt_decode_handler = api_settings.JWT_DECODE_HANDLER


def jwt_payload_handler(user):

    expiry = datetime.utcnow() + timedelta(days=2)

    payload = {
        'user_id': user.id,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'exp': expiry,
    }

    return payload
