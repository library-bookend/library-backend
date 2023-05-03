from rest_framework import serializers
from copies.models import Loan, Copy
from books.models import Book
from users.models import User
from django.shortcuts import get_object_or_404

class LoanSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        copy = get_object_or_404(Copy, pk=validated_data['copy_id'])
        user = get_object_or_404(User, email=validated_data['user_email'])
        loan = Loan.objects.create(copy=copy, user=user)

        loan.return_date = loan.loan_date + loan.book.loan_period
        

    
    

