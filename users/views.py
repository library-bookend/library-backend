from django.shortcuts import render
from rest_framework.pagination import PageNumberPagination
from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import User
from .serializers import UserSerializer
from .permissions import isEmployee


class UserView(generics.ListCreateAPIView, PageNumberPagination):
    authentication_classes = [JWTAuthentication]
    permission_classes = [isEmployee]

    queryset = User.objects.all()
    serializer_class = UserSerializer
