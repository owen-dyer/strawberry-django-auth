from typing import Any
import json

from django.http import HttpRequest
from strawberry.types import Info


def get_request(info: Info) -> HttpRequest | None:
    request: HttpRequest = info.context['request']
    if request is not None:
        return request
    return None


def get_header(request: HttpRequest, header: str) -> Any | None:
    return request.headers.get(header) or None
