import jwt

from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.utils import jwt_get_secret_key


def jwt_encode_handler(payload, secret_key=None):

    if secret_key:
        key = secret_key
    else:
        key = api_settings.JWT_PRIVATE_KEY or jwt_get_secret_key(payload)

    return jwt.encode(
        payload,
        key,
        api_settings.JWT_ALGORITHM
    ).decode('utf-8')


def jwt_decode_handler(token, key=None):
    options = {
        'verify_exp': api_settings.JWT_VERIFY_EXPIRATION,
    }
    # get user from token, BEFORE verification, to get user secret key
    unverified_payload = jwt.decode(token, None, False)

    if key:
        secret_key = key
    else:
        secret_key = api_settings.JWT_PUBLIC_KEY or jwt_get_secret_key(unverified_payload)

    return jwt.decode(
        token,
        secret_key,
        api_settings.JWT_VERIFY,
        options=options,
        leeway=api_settings.JWT_LEEWAY,
        audience=api_settings.JWT_AUDIENCE,
        issuer=api_settings.JWT_ISSUER,
        algorithms=[api_settings.JWT_ALGORITHM]
    )
