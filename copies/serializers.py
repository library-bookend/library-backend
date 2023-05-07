from rest_framework import serializers
from .models import Copy, Loan


class CopySerializer(serializers.ModelSerializer):
    class Meta:
        model = Copy
        fields = "__all__"


class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = "__all__"
