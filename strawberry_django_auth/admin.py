from django.contrib import admin

from strawberry_django_auth.models import RefreshToken

admin.site.register(RefreshToken)