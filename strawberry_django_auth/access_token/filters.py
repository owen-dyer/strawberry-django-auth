
import strawberry
import strawberry_django

from strawberry_django_auth.access_token.types import (
    AccessTokenAuthorizationType,
)


class Filters:
    # Might change this name to make it more 'correct' (might be authenticated idk)
    def is_authorized(token: str) -> AccessTokenAuthorizationType:
        pass
