from rest_framework import serializers
from.models import *

class SubscriptionPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPlan
        fields = '__all__'


class CreateOrderSerializer(serializers.Serializer):
    amount = serializers.IntegerField()
    currency = serializers.CharField()
   

class TransactionModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = ["payment_id", "order_id", "signature", "amount", "duration"]