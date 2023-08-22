import asyncio
from typing import Any, Optional, cast

from asgiref.sync import sync_to_async
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _
import jwt

from strawberry_django_auth import exceptions
from strawberry_django_auth.models import USER_MODEL
from strawberry_django_auth.settings import app_settings
from strawberry_django_auth.tokens import types


def encode_access_token(payload: types.PayloadType, _=None) -> str:
    token = jwt.encode(
        payload.__dict__,
        app_settings.ASYMMETRIC_PRIVATE_KEY or app_settings.SYMMETRIC_KEY,
        app_settings.JWT_ALGORITHM,
    )
    return cast(str, token)


def decode_access_token(token: str, _=None) -> types.PayloadType:
    return types.PayloadType(
        **jwt.decode(
            token,
            app_settings.ASYMMETRIC_PUBLIC_KEY or app_settings.SYMMETRIC_KEY,
            options={
                "verify_exp": app_settings.VERIFY_EXPIRATION,
                "verify_aud": app_settings.AUDIENCE is not None,
                "verify_signature": app_settings.VERIFY,
            },
            audience=app_settings.AUDIENCE,
            issuer=app_settings.ISSUER,
            algorithms=[app_settings.ALGORITHM],
        )
    )


def get_payload(token, context=None):
    try:
        return decode_access_token(token, context)
    except jwt.ExpiredSignatureError:
        raise exceptions.AccessTokenExpired()
    except jwt.DecodeError:
        raise exceptions.TokenAuthError(_("Error decoding signature"))
    except jwt.InvalidTokenError:
        raise exceptions.TokenAuthError(_("Invalid token"))


def get_uid_from_payload(payload):
    return getattr(payload, app_settings.USER_ID_CLAIM)


def get_user_by_natural_key(username):
    try:
        return USER_MODEL.objects.get_by_natural_key(username)
    except USER_MODEL.DoesNotExist:
        return None


async def get_user_by_natural_key_async(username):
    try:
        return await sync_to_async(USER_MODEL.objects.get_by_natural_key)(username)
    except USER_MODEL.DoesNotExist:
        return None


def get_user_from_payload(payload):
    user_id = get_uid_from_payload(payload)

    if not user_id:
        raise exceptions.TokenAuthError(_("Invalid payload"))

    user = get_user_by_natural_key(user_id)

    if user is not None and not getattr(user, "is_active", True):
        raise exceptions.TokenAuthError(_("User is disabled"))
    return user


async def get_user_from_payload_async(payload):
    user_id = get_uid_from_payload(payload)

    if not user_id:
        raise exceptions.TokenAuthError(_("Invalid payload"))

    user = await get_user_by_natural_key_async(user_id)

    if user is not None and not getattr(user, "is_active", True):
        raise exceptions.TokenAuthError(_("User is disabled"))
    return user


def get_user_by_token(token, context=None):
    payload = get_payload(token, context)
    return get_user_from_payload(payload)


async def get_user_by_token_async(token, context=None):
    payload = get_payload(token, context)
    return await get_user_from_payload_async(payload)
