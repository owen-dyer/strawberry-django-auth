from django.utils.translation import gettext_lazy as _


class TokenAuthError(Exception):
    message = ''

    def __init__(self, message: str = ''):
        if len(message) == 0:
            message = self.message
        super().__init__(message)


class PermissionDenied(TokenAuthError):
    message = _('You do not have permission to access this resource.')
    exception_code = _('permission_denied')
    gql_exception = [{
        'message': message,
        'exception_code': exception_code,
    }]


class AccessTokenExpired(TokenAuthError):
    message = _('Access token has expired')
    exception_code = _('access_expired')
    gql_exception = [{
        'message': message,
        'exception_code': exception_code,
    }]
