from typing import Optional

import strawberry
import strawberry_django

from strawberry_django_auth.settings import app_settings
from strawberry_django_auth.utils import inject_fields
from strawberry_django_auth.user.types import UserType


@strawberry.type
@inject_fields(
    {
        **({'iss': (str, '')} if app_settings.ISSUER else {}),
        **({'aud': (str, '')} if app_settings.AUDIENCE else {}),
        **({'exp': (int, 0)} if app_settings.EXPIRATION else {}),
        **({'iat': (int, 0)} if app_settings.ISSUED_AT or app_settings.ALLOW_REFRESH else {}),
        **({'jti': (str, '')} if app_settings.TOKEN_ID else {}),
    }
)
class PayloadType:
    sub: str = strawberry.UNSET


@strawberry.type
class AccessTokenType:
    token: str = strawberry.UNSET

@strawberry.type
class SubjectType:
    subject: str = strawberry.UNSET
    subject_object: Optional[UserType]

@strawberry.type
class AccessTokenAuthorizationType:
    authorized: bool = False
    subject: Optional[SubjectType]