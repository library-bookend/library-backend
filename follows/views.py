from books.models import Book
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from books.serializers import BookSerializer
from users.serializers import UserSerializer


class FollowDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        book = Book.objects.get(pk=pk)
        serializer = BookSerializer(book)
        users = serializer.data["followers"]
        user_serialized = UserSerializer(users, many=True)

        if request.user.is_employee:
            return Response({"count": book.followers.count(), "followers": user_serialized.data})

        return Response({"count": book.followers.count()})    

    def post(self, request, pk):
        book = Book.objects.get(pk=pk)
        book.followers.add(request.user)
        return Response(status=200)

    def delete(self, request, pk):
        book = Book.objects.get(pk=pk)
        book.followers.remove(request.user)
        return Response(status=204)
