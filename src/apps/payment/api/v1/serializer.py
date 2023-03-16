from rest_framework import serializers
from src.apps.payment.models import Payment

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ('id', 'user', 'course', 'amount', 'payment_type', 'payment_type', 'created_at')




