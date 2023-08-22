from datetime import datetime
import strawberry
import strawberry_django

from strawberry_django_auth.refresh_token import models
from strawberry_django_auth.user.types import UserType

@strawberry_django.type(model=models.RefreshToken)
class RefreshTokenTypeInternal:
    user: UserType
    token: str
    iat: datetime
    exp: datetime

@strawberry_django.type(model=models.RefreshToken)
class RefreshTokenType:
    token: str