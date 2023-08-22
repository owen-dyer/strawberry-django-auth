from typing import List, Optional

import strawberry
import strawberry_django
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import Group, Permission

@strawberry_django.type(model=Permission)
class PermissionType:
    name: str = strawberry.UNSET
    codename: str = strawberry.UNSET

@strawberry_django.type(model=Group)
class GroupType:
    name: str = strawberry.UNSET
    permissions: Optional[List[PermissionType]] = strawberry.UNSET

@strawberry_django.type(model=AbstractBaseUser)
class UserType:
    id: Optional[strawberry.ID] = strawberry.UNSET
    username: str = strawberry.UNSET
    is_authenticated: bool = False
    is_active: bool = False
    is_staff: bool = False
    is_superuser: bool = False
    groups: Optional[List[GroupType]] = strawberry.UNSET
    permissions: Optional[List[PermissionType]] = strawberry.UNSET