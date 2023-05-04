from rest_framework import serializers
from django.shortcuts import get_object_or_404

from copies.models import Loan


class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = ["return_date", "copy", "user"]
        read_only_fields = ["return_date", "copy", "user"]
