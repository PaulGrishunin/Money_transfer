from rest_framework import serializers
from .models import Client, Transaction


class GetClientSerializer(serializers.ModelSerializer):
    # money = serializers.DecimalField(decimal_places=2, max_digits=20,coerce_to_string=False)

    class Meta:
        model = Client
        fields = ('inn', 'clientname', 'money')


class ClientSerializer(serializers.ModelSerializer):
    # money = serializers.DecimalField(decimal_places=2, max_digits=20, coerce_to_string=False)

    class Meta:
        model = Client
        fields = ('inn', 'clientname', 'email', 'phone','address', 'money')


class TransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = ('id', 'sender', 'payee', 'amount', 'createdAt')