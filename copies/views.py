from django.shortcuts import render, get_object_or_404

from .models import Copy
from books.models import Book
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import generics
from library_bookend.permissions import IsEmployeeOrReadOnly

from .serializers import CopySerializer


class CopyView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsEmployeeOrReadOnly]
    serializer_class = CopySerializer

    def get_queryset(self):
        book_id = self.kwargs.get("book_id")
        book = get_object_or_404(Book, id=book_id)
        return Copy.objects.filter(book__id=book_id)
