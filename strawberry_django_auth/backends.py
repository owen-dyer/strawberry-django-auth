from django.contrib.auth.backends import BaseBackend
from strawberry_django_auth.helpers import (
    get_header,
)

from strawberry_django_auth.settings import app_settings

from strawberry_django_auth.access_token.helpers import (
    decode,
    get_token_subject,
)


class TokenAuthBackend(BaseBackend):
    def authenticate(self, request=None):
        access_token = get_header(request, app_settings.AUTH_HEADER_NAME)
        if access_token is None:
            return None
        print(f'Access Token: {access_token}')
        payload = decode(access_token)
        if payload is None:
            return None
        return get_token_subject(payload)

    def get_user(self, user_id):
        return None
