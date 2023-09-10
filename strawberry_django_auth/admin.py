from django.contrib import admin

from strawberry_django_auth.models import RefreshToken

class RefreshTokenAdmin(admin.ModelAdmin):
    
    fieldsets = [
        (
            None,
            {
                'fields': (
                    'user',
                )
            }
        ),
        (
            'Token',
            {
                'fields': (
                    'token',
                )
            }
        ),
        (
            'Token Information',
            {
                'fields': (
                    'iat',
                    'exp',
                )
            }
        )
    ]
    readonly_fields = ('user', 'token', 'iat', 'exp',)

admin.site.register(RefreshToken, RefreshTokenAdmin)