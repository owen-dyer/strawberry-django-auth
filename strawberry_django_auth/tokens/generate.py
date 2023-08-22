import jwt
import secrets
from django.contrib.auth.base_user import AbstractBaseUser

from strawberry_django_auth.settings import app_settings
from strawberry_django_auth.tokens.types import AccessTokenType


class AccessToken:

    def generate(user: AbstractBaseUser) -> AccessTokenType:
        user_id = app_settings.USER_ID_FIELD
        # id_claim = {user_id: getattr(user.user, user_id)}
        # print(f'User ID: {user_id} ID Claim: {id_claim}')
        return 'token generated'


class RefreshToken:
    pass
