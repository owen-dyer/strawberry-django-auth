from typing import Optional

import strawberry
import strawberry_django

from strawberry_django_auth import models
from strawberry_django_auth.access_token import types as access_token_types
from strawberry_django_auth.refresh_token import types as refresh_token_types

# Need to add support for additional fields (e.g. email, phone number, etc.)
@strawberry_django.input(model=models.USER_MODEL)
class LoginInput:
    username: str
    password: str

@strawberry.type
class TokenType:
    success: bool = False
    access_token: Optional[access_token_types.AccessTokenType]
    refresh_token: Optional[refresh_token_types.RefreshTokenType]
    error: Optional[str]