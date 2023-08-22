import strawberry
import strawberry_django
from strawberry_django.optimizer import DjangoOptimizerExtension

# from django_gql_jwt.tokens import resolvers

from strawberry_django_auth.user.types import UserType
import strawberry_django_auth.mutations as auth_mutations


@strawberry.type
class Query:
    users: list[UserType] = strawberry_django.field()


@strawberry.type
class Mutation:
    authenticate = auth_mutations.ObtainAccessToken.obtain


schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
    extensions=[
        DjangoOptimizerExtension,
    ],
)
