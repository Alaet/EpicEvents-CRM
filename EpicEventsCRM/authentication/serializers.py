from rest_framework import serializers

from authentication.models import User


class UserCreation(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'last_name', 'email', 'password', 'team']
        extra_kwargs = {
            'password': {'write_only': True},
            }
