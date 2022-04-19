from django.contrib.auth.models import Group

from rest_framework import filters
from rest_framework.exceptions import NotFound
from rest_framework.viewsets import ModelViewSet

from EpicEventsCRM.permissions import IsMainContact, IsStaff
from event.models import Event
from event.serializers import EventListSerializer


class EventViewSet(ModelViewSet):

    serializer_class = EventListSerializer
    search_fields = ['client__company_name', '=client__email', '=event_date']
    filter_backends = (filters.SearchFilter,)

    def get_queryset(self):
        sales_team = Group.objects.get(name="SalesTeam")
        events = Event.objects.filter(support_contact=self.request.user.id)
        if self.request.user.groups == sales_team:
            return Event.objects.filter(contract__sales_contact=self.request.user.id)
        elif self.request.user.is_superuser:
            return Event.objects.all()
        elif not events:
            raise NotFound("Il n'existe aucun évènement qui vous est lié.")
        return Event.objects.filter(id__in=events)

    def get_permissions(self):
        permission_classes = [IsMainContact]
        if self.request.method == "GET":
            permission_classes = [
                IsStaff
            ]
        elif self.request.method in ["PUT", "PATCH"]:
            permission_classes = [
                IsMainContact
            ]
        elif self.request.method == "DELETE":
            permission_classes = [
                IsMainContact
            ]
        return [permission() for permission in permission_classes]
