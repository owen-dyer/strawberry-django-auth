
import strawberry
from strawberry.types import Info
import strawberry_django

from django.contrib.auth import authenticate

from strawberry_django_auth.settings import app_settings
from strawberry_django_auth.types import (
    LoginInput,
    TokenType
)
from strawberry_django_auth.access_token.methods import (
    AccessToken
)
from strawberry_django_auth.helpers import (
    get_request,
    get_header,
)
from strawberry_django_auth import exceptions
from strawberry_django_auth.refresh_token.models import RefreshToken


class Authenticate:
    @strawberry.mutation
    def method(self, info: Info, credentials: LoginInput) -> TokenType:
        response = TokenType
        request = get_request(info)
        user = authenticate(
            request,
            username=credentials.username,
            password=credentials.password
        )
        if user is None:
            response.success = False
            response.error = exceptions.InvalidCredentials.message
            return response
        response.success = True
        response.access_token = AccessToken.create(user.get_username())
        response.refresh_token = RefreshToken.objects.create(
            user=user,
        )
        return response


class VerifyAccessToken:
    @strawberry.mutation
    def method(self, info: Info) -> bool:
        request = get_request(info)
        access_token = get_header(request, app_settings.AUTH_HEADER_NAME)
        if access_token is None:
            return False
        return AccessToken.verify(access_token)


class RefreshAccessToken:
    pass
