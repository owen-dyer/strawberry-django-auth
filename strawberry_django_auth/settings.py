from django.conf import settings
from django.contrib.auth import get_user_model
from django.test.signals import setting_changed
from django.utils.module_loading import import_string

from dataclasses import dataclass
from datetime import timedelta

DEFAULT_SETTINGS = {
    'ALGORITHM': 'HS256',
    'SYMMETRIC_KEY': settings.SECRET_KEY,
    'ASYMMETRIC_PRIVATE_KEY': '',
    'ASYMMETRIC_PUBLIC_KEY': '',
    'TIMESTAMP_FORMAT': '%Y-%m-%d %H:%M:%S.%f',
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=10),
    'ALLOW_REFRESH': False,
    'REFRESH_TOKEN_LIFETIME': timedelta(hours=6),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'AUTH_HEADER_TYPES': 'Bearer',
    'AUTH_HEADER_NAME': 'Authorization',
    'USER_ID_FIELD': get_user_model().USERNAME_FIELD,
    'USER_ID_CLAIM': 'user_id',
    'REQUIRE_VERIFICATION': False,
    'TOKEN_OBTAIN_HANDLER': '',
    'TOKEN_REFRESH_HANDLER': '',
    'TOKEN_VERIFY_HANDLER': '',
    'TOKEN_BLACKLIST_HANDLER': '',
    'ALLOW_ALL_CLASSES': (),
    'VERIFY': True,
    'ROTATE_CSRF_TOKEN': True,

    # Claims for token payload
    'ISSUER': False,
    'SUBJECT': True,
    'AUDIENCE': False,
    'EXPIRATION': True,
    'ISSUED_AT': True,
    'TOKEN_ID': False,
}

IMPORT_STRINGS = (
    'TOKEN_OBTAIN_HANDLER',
    'TOKEN_REFRESH_HANDLER',
    'TOKEN_VERIFY_HANDLER',
    'TOKEN_BLACKLIST_HANDLER',
    'ALLOW_ALL_CLASSES',
)


def perform_import(value, setting_name):
    if isinstance(value, str):
        return import_from_string(value, setting_name)
    if isinstance(value, (list, tuple)):
        return [import_from_string(item, setting_name) for item in value]
    return value


def import_from_string(value, setting_name):
    try:
        return import_string(value)
    except ImportError as e:
        msg = f'Could not import {value} for JWT setting {setting_name}.' f'{e.__class__.__name__}: {e}.'
        raise ImportError(msg)


class AppSettings:
    def __init__(self, defaults, import_strings):
        self.defaults = defaults
        self.import_strings = import_strings
        self._cached_attrs = set()

    def __getattr__(self, attr):
        if attr not in self.defaults:
            raise AttributeError(f'Invalid setting: {attr}')
        value = self.project_settings.get(attr, self.defaults[attr])

        if attr == 'ALLOW_ALL_CLASSES':
            value = list(value) + [
                'value for access token mixin'
            ]
        if attr in self.import_strings:
            value = perform_import(value, attr)

        self._cached_attrs.add(attr)
        setattr(self, attr, value)
        return value

    @property
    def project_settings(self):
        if not hasattr(self, '_project_settings'):
            self._project_settings = getattr(
                settings, 'TOKEN_AUTH_SETTINGS', {}
            )
        return self._project_settings

    def reload(self):
        for attr in self._cached_attrs:
            delattr(self, attr)

        self._cached_attrs.clear()

        if hasattr(self, '_project_settings'):
            delattr(self, '_project_settings')


def reload_settings(*args, **kwargs):
    setting = kwargs['setting']
    if setting == 'TOKEN_AUTH_SETTINGS':
        app_settings.reload()


setting_changed.connect(reload_settings)

app_settings = AppSettings(DEFAULT_SETTINGS, IMPORT_STRINGS)
