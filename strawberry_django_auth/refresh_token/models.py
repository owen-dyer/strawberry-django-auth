import secrets
import uuid
from datetime import datetime, timezone

from django.db import models
from django.conf import settings


class RefreshToken(models.Model):
    def generate():
        # Need to add setting for the number of bytes/length
        return secrets.token_hex(16)

    # Primary key for refresh token
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    # User refresh token is assigned to
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='refresh_tokens',
        related_query_name='refresh_token',
    )
    # Refresh token
    token = models.CharField(
        max_length=255,
        unique=True,
        editable=False,
        default=generate,
    )
    # Creation timestamp for this token
    iat = models.DateTimeField(
        auto_now_add=True,
    )
    # Revocation timestamp for this token
    exp = models.DateTimeField(
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.token

    # Need to add method so the token that gets saved in the DB gets hashed...
    # and the one that gets sent to the client doesn't
    def save(self, *args, **kwargs):
        if not self.token:
            self.token = self._cached_token = self.generate()
        print(f'Refresh Token: {self.token}')

        super().save(*args, **kwargs)

    def get(self):
        if hasattr(self, '_cached_token'):
            return self._cached_token
        return self.token

    def revoke(self, token: str):
        self.exp = datetime.now(timezone.utc)
        self.save()

    def rotate(self, token: str):
        self.revoke(token)
        RefreshToken.objects.create(
            user=self.user,
        )
