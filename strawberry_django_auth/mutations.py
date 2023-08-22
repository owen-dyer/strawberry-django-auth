

import strawberry
from strawberry.types import Info
import strawberry_django

from strawberry_django_auth.settings import app_settings
from strawberry_django_auth.types import (
    LoginInput
)
from strawberry_django_auth.access_token.methods import (
    AccessToken
)
from strawberry_django_auth.access_token.types import (
    AccessTokenType
)
from strawberry_django_auth.helpers import get_request, get_header


class ObtainAccessToken:
    @strawberry.mutation
    def obtain(self, info: Info, credentials: LoginInput) -> AccessTokenType:
        request = get_request(info)
        header = get_header(request, app_settings.AUTH_HEADER_NAME)
        print(f'Auth Header: {header}')
        access_token = AccessToken.create(subject='test_subject')
        return access_token
