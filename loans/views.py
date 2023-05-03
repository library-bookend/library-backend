from django.shortcuts import render
from rest_framework import generics
from .models import Loan
from rest_framework_simplejwt.authentication import JWTAuthentication
from users.permissions import IsEmployeeOrReadOnly
from .serializers import Loan


class LoanView(generics.ListCreateAPIView):
    permission_classes = []
    authentication_classes = []
    queryset = Loan.objects.all()
    serializer_class = Loan

    def get_queryset(self):
        return Loan.objects.filter(user=self.request.user)
