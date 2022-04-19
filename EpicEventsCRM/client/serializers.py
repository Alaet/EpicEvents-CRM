from rest_framework.serializers import ModelSerializer

from client.models import Client
from contract.serializers import ContractListSerializer


class ClientListSerializer(ModelSerializer):

    client_contract = ContractListSerializer(read_only=True, many=True)

    class Meta:
        model = Client
        fields = '__all__'
        extra_kwargs = {
            'sales_contact': {'read_only': True},
        }
