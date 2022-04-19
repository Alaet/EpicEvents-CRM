from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from authentication.serializers import UserCreation
from event.models import Event


class EventListSerializer(ModelSerializer):

    support_contact = SerializerMethodField('get_support_contact')

    def get_support_contact(self, obj):
        user = self.context['request'].user
        serializer = UserCreation(user, context=self.context)
        return serializer.data

    class Meta:
        model = Event
        fields = '__all__'
        extra_kwargs = {
                    'contract': {'read_only': True},
                }
