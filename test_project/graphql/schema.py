from typing import Any, List
import strawberry
import strawberry_django
from strawberry_django.optimizer import DjangoOptimizerExtension

from strawberry_django_auth.user.types import UserType
from strawberry_django_auth import mutations
from strawberry_django_auth.access_token.filters import IsAuthenticated


@strawberry.type
class Query:
    users: List[UserType] = strawberry_django.field(
        permission_classes=[IsAuthenticated]
    )


@strawberry.type
class Mutation:
    login = mutations.Authenticate.method
    verify_token = mutations.VerifyAccessToken.method


schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
    extensions=[
        DjangoOptimizerExtension,
    ]
)
