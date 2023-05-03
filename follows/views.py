from .models import Book
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from library_bookend.permissions import isEmployeeOrReadOnly


class FollowDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        book = Book.objects.get(pk=pk)
        return Response({"count": book.followers.count(), "followers": book.followers.all()})

    def post(self, request, pk):
        book = Book.objects.get(pk=pk)
        book.followers.add(request.user)
        return Response(status=200)

    def delete(self, request, pk):
        book = Book.objects.get(pk=pk)
        book.followers.remove(request.user)
        return Response(status=204)
