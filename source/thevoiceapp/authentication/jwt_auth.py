import jwt

from django.utils.translation import ugettext as _
from django.utils.encoding import smart_text
from django.utils.six import text_type


from rest_framework import HTTP_HEADER_ENCODING
from rest_framework import exceptions
from rest_framework.authentication import (
    get_authorization_header
)
from rest_framework_jwt.authentication import BaseJSONWebTokenAuthentication
from rest_framework_jwt.settings import api_settings

from thevoiceapp.models import User
from thevoiceapp.authentication.jwt_utils import jwt_decode_handler


class JSONWebTokenAuthentication(BaseJSONWebTokenAuthentication):
    JWT_SECRET = None

    def get_jwt_value(self, request, header_prefix=None):

        auth = request.META.get(u'HTTP_X_JWT', b'').split()

        if isinstance(auth, text_type):
            # Work around django test client oddness
            auth = auth.encode(HTTP_HEADER_ENCODING)

        if header_prefix:
            auth_header_prefix = header_prefix
        else:
            auth_header_prefix = api_settings.JWT_AUTH_HEADER_PREFIX.lower()

        if not auth or smart_text(auth[0].lower()) != auth_header_prefix:

            auth = get_authorization_header(request).split()
            auth_header_prefix = api_settings.JWT_AUTH_HEADER_PREFIX.lower()

            if not auth or smart_text(auth[0].lower()) != auth_header_prefix:
                return None

        if len(auth) == 1:
            msg = _('Invalid Authorization header. No credentials provided.')
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = _('Invalid Authorization header. Credentials string '
                    'should not contain spaces.')
            raise exceptions.AuthenticationFailed(msg)

        return auth[1]

    def jwt_authenticate_credentials(self, payload):
        """
        Returns an active user that matches the payload's user id.
        """
        try:
            user = User.objects.get(id=payload['user_id'])
        except User.DoesNotExist:
            msg = _('Invalid signature.')
            raise exceptions.AuthenticationFailed(msg)

        return user

    def authenticate(self, request):
        """
        Returns a two-tuple of `User` and token if a valid signature has been
        supplied using JWT-based authentication.  Otherwise returns `None`.
        """
        jwt_value = self.get_jwt_value(request)
        if jwt_value is None:
            return None

        try:
            payload = jwt_decode_handler(jwt_value, self.JWT_SECRET)
        except jwt.ExpiredSignature:
            msg = _('Signature has expired.')
            raise exceptions.AuthenticationFailed(msg)
        except jwt.DecodeError:
            msg = _('Error decoding signature.')
            raise exceptions.AuthenticationFailed(msg)
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed()

        if payload.get('referee', False):
            raise exceptions.AuthenticationFailed()

        user = self.jwt_authenticate_credentials(payload)

        return user, jwt_value

    def authenticate_header(self, request):
        """
        Return a string to be used as the value of the `WWW-Authenticate`
        header in a `401 Unauthenticated` response, or `None` if the
        authentication scheme should return `403 Permission Denied` responses.
        """
        return '{0} realm="{1}"'.format(api_settings.JWT_AUTH_HEADER_PREFIX, self.www_authenticate_realm)
