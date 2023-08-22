import inspect

from django.contrib.auth import get_user_model, authenticate
import strawberry
from strawberry.field import StrawberryField
from strawberry.types import Info


from strawberry_django_auth.tokens import mixins
# from strawberry_django_auth.decorators import (
#     token_auth
# )
from strawberry_django_auth.types import (
    TokenType,
    LoginInput,
)

__all__ = [
    'ObtainAccessTokenMutation',
    'ObtainAccessToken',
]

from strawberry_django_auth.utils import (
    create_strawberry_argument,
    get_context,
)

from strawberry_django_auth.access_token.methods import AccessToken
from strawberry_django_auth.access_token.types import AccessTokenType


class ObtainAccessToken:
    @strawberry.mutation
    def obtain(self, info: Info, credentials: LoginInput) -> AccessTokenType:
        access_token = AccessToken.create(subject='test_subject')
        return access_token
        # context = get_context(info)
        # username = credentials.username
        # password = credentials.password
        # user = authenticate(request=context, username=username, password=password)
        # if user is None:
        #     return TokenType(
        #         success=False,
        #     )
        # print(f'{user.get_username()} successfully logged in')
        # print(f'Obtaining token for {credentials.username}')
        # return TokenType(
        #     success=True
        # )


class ObtainAccessTokenAsync(ObtainAccessToken):
    # Decorators handle async implementation, just here for consistency
    pass
