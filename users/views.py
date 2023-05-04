from django.shortcuts import render, get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth import login
from django.utils import timezone

from .models import User
from copies.models import Loan
from loans.serializers import LoanSerializer
from .serializers import UserSerializer
from library_bookend.permissions import isEmployee, isOwnerOrEmployee


class CustomLoginView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        user = User.objects.get(username=self.request.data["username"])

        if user.blocked_until is not None and user.blocked_until <= timezone.now():
            user.blocked_until = None
            user.save()
            login(request, user)
            return response
        return response


class UserView(generics.ListCreateAPIView, PageNumberPagination):
    authentication_classes = [JWTAuthentication]
    permission_classes = [isEmployee]

    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserLoansView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, isOwnerOrEmployee]

    serializer_class = LoanSerializer

    def get_queryset(self):
        user_id = self.kwargs.get("user_id")
        user = get_object_or_404(User, id=user_id)
        self.check_object_permissions(self.request, user)
        queryset = Loan.objects.filter(user__id=user_id)
        return queryset
