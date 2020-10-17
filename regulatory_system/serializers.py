from rest_framework import serializers
from regulatory_system.models import AbnormalFlow, AbnormalFlowDetail, Customer, CustomerLatest


class AbnormalFlowSerializer(serializers.ModelSerializer):
    class Meta:
        model = AbnormalFlow
        fields = '__all__'


class AbnormalFlowDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = AbnormalFlowDetail
        fields = '__all__'


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class CustomerLatestSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerLatest
        fields = '__all__'
