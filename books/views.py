from rest_framework.views import APIView, Response
from .models import Album
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from users.permissions import isEmployee
from .models import Book
from .serializers import BookSerializer


class BookView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [isEmployee]

    queryset = Book.objects.all()
    serializer_class = BookSerializer



class FollowView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        followings = user.following.all()
        return Response(followings)


class FollowDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, book_id):
        user = request.user
        book = Album.objects.get(pk=book_id)
        if book.followers.filter(pk=user.id).exists():
            book.followers.remove(user)
            return Response({"message": "unfollowed"})
        else:
            book.followers.add(user)
            return Response({"message": "followed"})
