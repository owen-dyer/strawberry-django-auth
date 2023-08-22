from functools import wraps
import inspect

from django.core.handlers.asgi import ASGIRequest
from django.contrib import auth
from django.middleware.csrf import rotate_token
from django.utils.translation import gettext as _

from strawberry.types import Info

from strawberry_django_auth.auth import authenticate
from strawberry_django_auth.settings import app_settings
from strawberry_django_auth.utils import (
    get_context,
)
from strawberry_django_auth import exceptions


__all__ = [
    'dispose_extra_kwargs'
]


# def token_auth(f):
#     async def wrapper_async(cls, info: Info, credentials: TokenInput):
#         context = get_context(info)
#         context.token_auth = True
#         user = await authenticate(
#             request=context,
#             username=credentials.username,
#             password=credentials.password,
#         )
#         if user is None:
#             raise exceptions.TokenAuthError(
#                 _('Provided credentials invalid'),
#             )
#         context.user = user
#         print(f'{user.get_username()} authenticated (async)')
#         result = f(cls, info, credentials)

#     @wraps(f)
#     @csrf_rotation
#     def wrapper(cls, info: Info, credentials: TokenInput):
#         context = get_context(info)
#         if inspect.isawaitable(f) or isinstance(context, ASGIRequest):
#             return wrapper_async(cls, info, credentials)
#         context.token_auth = True
#         user = auth.authenticate(
#             request=context,
#             username=credentials.username,
#             password=credentials.password,
#         )
#         if user is None:
#             raise exceptions.TokenAuthError(
#                 _('Provided credentials invalid'),
#             )
#         context.user = user
#         print(f'{user.get_username()} authenticated (sync)')
#         result = f(cls, info, credentials)
    
#     return wrapper


# def csrf_rotation(f):
#     @wraps(f)
#     def wrapper(cls, info: Info, *args, **kwargs):
#         if app_settings.ROTATE_CSRF_TOKEN:
#             rotate_token(info.context)
#         return f(cls, info, **kwargs)

#     return wrapper
