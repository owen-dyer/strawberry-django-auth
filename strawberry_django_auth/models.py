from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models

from strawberry_django_auth.refresh_token.models import (
    RefreshToken,
)

USER_MODEL = get_user_model()