from rest_framework.serializers import ModelSerializer

from contract.models import Contract


class ContractListSerializer(ModelSerializer):

    class Meta:
        model = Contract
        extra_kwargs = {
            'status': {'help_text': 'Active'},
            'sales_contact': {'read_only': True},
            'contract_event': {'read_only': True},
        }
        fields = ('id', 'status', 'amount', 'payment_due', 'sales_contact', 'client', 'contract_event',)
