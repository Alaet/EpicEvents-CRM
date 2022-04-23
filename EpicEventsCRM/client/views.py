from rest_framework import filters
from rest_framework.viewsets import ModelViewSet

from EpicEventsCRM.permissions import IsMainContact, IsStaff
from client.models import Client
from client.serializers import ClientListSerializer
from event.models import Event


class ClientViewSet(ModelViewSet):

    serializer_class = ClientListSerializer
    search_fields = ['company_name', '=email']
    filter_backends = (filters.SearchFilter,)

    def get_queryset(self):
        events = Event.objects.filter(support_contact=self.request.user.id).values_list('client', flat=True)
        contact = Client.objects.filter(sales_contact=self.request.user.id)

        user_client = Client.objects.filter(pk__in=events)
        if contact:
            return contact
        if user_client:
            return user_client
        return Client.objects.all()

    def get_permissions(self):
        permission_classes = [IsMainContact]
        if self.request.method == "GET":
            permission_classes = [
                IsStaff,
            ]
        elif self.request.method == "POST":
            permission_classes = [
                IsMainContact
            ]
        elif self.request.method in ["PUT", "PATCH", "DELETE"]:
            permission_classes = [
                IsMainContact
            ]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(sales_contact=user)
