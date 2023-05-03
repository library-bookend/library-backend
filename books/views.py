from django.shortcuts import render
from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication

from users.permissions import isEmployee
from .models import Book
from .serializers import BookSerializer


class BookView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [isEmployee]

    queryset = Book.objects.all()
    serializer_class = BookSerializer


