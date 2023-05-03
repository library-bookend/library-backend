from django.views import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from users.permissions import IsEmployeeOrReadOnly
from books.models import Book
from books.serializers import BookSerializer
from rest_framework.pagination import PageNumberPagination


class BookView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsEmployeeOrReadOnly]
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    pagination_class = PageNumberPagination

class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsEmployeeOrReadOnly]
    queryset = Book.objects.all()
    serializer_class = BookSerializer
