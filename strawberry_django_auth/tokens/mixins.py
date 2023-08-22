import inspect
from typing import Any, Dict, Optional, Type, Union

import strawberry
from strawberry.field import StrawberryField
from strawberry.types import Info
from strawberry_django.fields.field import StrawberryDjangoField

from strawberry_django_auth import settings
from strawberry_django_auth.tokens.fields import (
    StrawberryDjangoRefreshTokenField,
    StrawberryDjangoTokenField,
)

from strawberry_django_auth.utils import (
    create_strawberry_argument,
    get_context,
)


class BaseTokenMixin:
    @staticmethod
    def init_fields(cls, field_options: Dict[str, Dict[str, Any]]):
        for (__, field) in inspect.getmembers(cls, lambda fld: isinstance(fld, StrawberryField)):
            if field.type_annotation is None and isinstance(field, StrawberryDjangoField):
                # StrawberryDjangoFields resolve their arguments after strawberry decorator is applied.
                # It is necessary to add subclasses to the field class which provide required arguments when
                #   fields are collected.
                base_types = StrawberryDjangoField, StrawberryDjangoTokenField
                if settings.app_settings.ALLOW_REFRESH:
                    new_type = type(
                        'StrawberryDjangoJWTField',
                        (
                            *base_types,
                            StrawberryDjangoRefreshTokenField,
                        ),
                        {},
                    )
                else:
                    new_type = type('StrawberryDjangoJWTField', base_types, {})
                field.__class__ = new_type
                continue
            field.arguments.append(create_strawberry_argument(
                'access_token', 'accessToken', str, **field_options.get('access_token', {})))
            if settings.app_settings.ALLOW_REFRESH:
                field.arguments.append(create_strawberry_argument(
                    'refresh_token', 'refreshToken', str, **field_options.get('refresh_token', {})))


class TokenMixin(BaseTokenMixin):
    def __init_subclass__(cls, **kwargs):
        cls.init_fields(
            cls,
            {
                'access_token': {
                    'is_optional': True,
                },
                'refresh_token': {
                    'is_optional': True,
                },
            }
        )
