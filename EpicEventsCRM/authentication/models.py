from django.contrib.auth.models import AbstractUser, Group
from django.db.models import ForeignKey, SET_NULL


class User(AbstractUser):
    groups = ForeignKey(Group, related_name='user_role', on_delete=SET_NULL, null=True)
