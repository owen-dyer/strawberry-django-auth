import strawberry
import strawberry_django
from strawberry.field import StrawberryField
from typing import Callable
from strawberry.types import Info

from ..settings import Settings
from .types import (
    ObtainAccessTokenInput,
    ObtainAccessTokenType,
)


class BaseMixin:
    field: StrawberryField
    resolve_mutation: Callable


class ObtainAccessToken(BaseMixin):
    # User login request will be resolved by this class
    '''@classmethod
    def resolve_mutation(cls, info, credentials: ObtainAccessTokenInput) -> ObtainAccessTokenType:
        print(f'Verification Required: {Settings.REQUIRE_VERIFICATION}')
        if Settings.REQUIRE_VERIFICATION:
            # Check whether the user is verified or not (jwt user extension)
            print('Verification Required!')
        return ObtainAccessTokenType.authenticate(info, credentials)'''


class RefreshAccessToken:
    # User refresh request will be resolved by this class
    pass


class VerifyAccessToken:
    # Access token will be verified in this class
    pass


class BlacklistRefreshToken:
    # Refresh tokens will be blacklisted in this class
    pass
