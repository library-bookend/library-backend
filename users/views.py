from django.shortcuts import render
from rest_framework.pagination import PageNumberPagination
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView

from django.contrib.auth import login
from django.utils import timezone

from .models import User
from .serializers import UserSerializer
from .permissions import isEmployee


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

    def can_borrow(self, user):
        if user.status == "blocked" and user.blocked_until is not None and user.blocked_until > timezone.now():
            return False
        return True

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        headers = self.get_success_headers(serializer.data)

        if not self.can_borrow(user):
            user.delete()
            return Response({"detail": "User is blocked"}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)