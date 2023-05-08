from .models import Book
from drf_spectacular.utils import extend_schema
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import generics, request
from library_bookend.permissions import IsEmployeeOrReadOnly
from .serializers import BookSerializer


class BookView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsEmployeeOrReadOnly]

    serializer_class = BookSerializer

    @extend_schema(
        description="Pass the parameter 'recents=true' in the url to return the last books added"
    )
    def get_queryset(self):
        if "recents" in self.request.query_params:
            queryset = Book.objects.order_by("-id")[:5]
        else:
            queryset = Book.objects.all()
        return queryset
