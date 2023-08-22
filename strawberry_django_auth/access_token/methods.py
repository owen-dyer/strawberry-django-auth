from datetime import datetime
from typing import Dict

import strawberry
import strawberry_django

from strawberry_django_auth.access_token.types import (
    AccessTokenType,
    PayloadType,
)
from strawberry_django_auth.settings import app_settings
from strawberry_django_auth.access_token.helpers import (
    decode,
    encode,
)


class AccessToken:
    # TODO: Automate this with classes for payload claims/stuff in settings
    # Also, add this in later because I'm lazy rn lol
    # def create_payload(self) -> Dict[]:
    #     pass

    def create(subject: str) -> AccessTokenType:
        payload = {
            'sub': subject,
        }

        if app_settings.ISSUER:
            payload['iss'] = 'example_issuer'

        if app_settings.AUDIENCE:
            payload['aud'] = 'example_audience'

        if app_settings.ISSUED_AT:
            payload['iat'] = datetime.utcnow().timestamp()

        if app_settings.EXPIRATION:
            if app_settings.ISSUED_AT:
                payload['exp'] = payload['iat'] + \
                    app_settings.ACCESS_TOKEN_LIFETIME.total_seconds()
            else:
                payload['exp'] = datetime.utcnow().timestamp(
                ) + app_settings.ACCESS_TOKEN_LIFETIME.total_seconds()

        if app_settings.TOKEN_ID:
            payload['jti'] = 'some_function_that_generates_a_random_id'

        payload_type = PayloadType(**payload)

        return AccessTokenType(
            token=encode(payload_type)
        )
    
    