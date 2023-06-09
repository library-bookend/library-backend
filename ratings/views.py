from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from books.models import Book
from django.db.models import Sum
from rest_framework.response import Response
from .serializers import RatingSerializer


class RatingsDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = RatingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        book = Book.objects.get(id=request.data["book_id"])
        user = request.user

        if book.rating.filter(user=user).exists():
            return Response("You have already rated this book", status=400)

        book.rating.create(user=user, rating=request.data["rating"])

        return Response("You rated this book successfully")
