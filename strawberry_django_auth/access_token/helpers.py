from typing import Any, Dict
import jwt

from strawberry_django_auth.settings import app_settings
from strawberry_django_auth.access_token.types import PayloadType


def encode(payload: PayloadType) -> str:
    return jwt.encode(
        payload.__dict__,
        app_settings.SYMMETRIC_KEY or app_settings.ASYMMETRIC_PRIVATE_KEY,
        app_settings.ALGORITHM,
    )


def decode(token: str) -> PayloadType:
    return PayloadType(
        **jwt.decode(
            jwt=token,
            key=app_settings.SYMMETRIC_KEY or app_settings.ASYMMETRIC_PRIVATE_KEY,
            algorithms=app_settings.ALGORITHM,
            options={
                'verify_signature': app_settings.VERIFY,
                'verify_exp': app_settings.EXPIRATION,
            },
            leeway=0,
        )
    )

def get_token_from_header(header: Dict[str, Any]) -> str:
    pass