
from typing import Any, Awaitable, Union
import strawberry
from strawberry.permission import BasePermission
from strawberry.types import Info
from strawberry.types.info import Info
import strawberry_django

from strawberry_django_auth.access_token.types import (
    AccessTokenAuthorizationType,
)

from strawberry_django_auth.helpers import get_request, get_header
from strawberry_django_auth.settings import app_settings
from strawberry_django_auth.access_token.helpers import decode

class IsAuthenticated(BasePermission):
    message = "User is not authorized to access this resource"

    def has_permission(self, source: Any, info: Info, **kwargs: Any) -> bool | Awaitable[bool]:
        request = get_request(info)
        access_token = get_header(request, app_settings.AUTH_HEADER_NAME)
        if access_token is None:
            return False
        subject = decode(access_token)
        if subject is None:
            return False
        print(f'Subject: {subject}')
        return True