from rest_framework import filters
from rest_framework.viewsets import ModelViewSet

from EpicEventsCRM.permissions import IsMainContact

from contract.models import Contract
from contract.serializers import ContractListSerializer
from event.models import Event


class ContractViewSet(ModelViewSet):

    serializer_class = ContractListSerializer
    permission_classes = [IsMainContact]
    search_fields = ['id', 'client__company_name', '=client__email', '=date_created', 'amount']
    filter_backends = (filters.SearchFilter,)

    def get_queryset(self):
        events = Event.objects.filter(support_contact=self.request.user.id).values_list('contract', flat=True)
        contact = Contract.objects.filter(sales_contact=self.request.user.id)
        user_client = Contract.objects.filter(pk__in=events)
        if contact:
            return contact
        if user_client:
            return user_client
        return Contract.objects.all()

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(sales_contact=user)
