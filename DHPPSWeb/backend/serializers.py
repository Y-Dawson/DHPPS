from rest_framework import serializers
from backend.models import Accountinformation


class AccountsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accountinformation
        fields = '__all__'
