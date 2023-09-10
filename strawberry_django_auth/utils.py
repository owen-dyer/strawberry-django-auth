from __future__ import annotations

import asyncio

from typing import TYPE_CHECKING, Any, Optional, cast, TypeVar, Dict, Tuple, Type

from django.http import HttpRequest
from graphql import GraphQLResolveInfo
from strawberry.annotation import StrawberryAnnotation
from strawberry.arguments import StrawberryArgument
from strawberry.django.context import StrawberryDjangoContext
from strawberry.types import Info

from strawberry_django_auth.settings import app_settings


def create_strawberry_argument(python_name: str, graphql_name: str, arg_type: type[Any], **options):
    return StrawberryArgument(
        python_name,
        graphql_name,
        StrawberryAnnotation(create_argument_type(
            arg_type, **options
        )),
    )


def create_argument_type(arg_type: type[Any], **options):
    if options.get('is_optional'):
        return Optional[arg_type]
    return arg_type


# need to put this into graphql view and then can prob change a lot of code uggg but its the intended way...
def get_context(info: HttpRequest | Info[Any, Any] | GraphQLResolveInfo) -> Any:
    if hasattr(info, 'context'):
        ctx = getattr(info, 'context')
        if isinstance(ctx, StrawberryDjangoContext):
            return ctx.request
        return ctx
    return info


X = TypeVar('X', Any, Any)


def inject_fields(fields: dict[str, Tuple[Type[X], X]]):
    def inject(cls):
        for field, data in fields.items():
            setattr(cls, field, data[1])
            cls.__annotations__[field] = data[0]
        return cls

    return inject
