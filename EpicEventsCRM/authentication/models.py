from django.contrib.auth.models import AbstractUser
from django.db.models import CharField


class User(AbstractUser):
    choices = (
        ('sales', 'Sales'),
        ('support', 'Support'),
    )

    team = CharField(max_length=50, choices=choices)
