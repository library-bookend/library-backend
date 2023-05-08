from django.shortcuts import render, get_object_or_404
import datetime
from .models import Copy, Loan
from books.models import Book
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import generics
from library_bookend.permissions import IsEmployeeOrReadOnly
from django.http import HttpResponse
from .serializers import CopySerializer
from loans.serializers import LoanSerializer
from users.models import User
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class CopyView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsEmployeeOrReadOnly]
    serializer_class = CopySerializer

    def get_queryset(self):
        book_id = self.kwargs.get("book_id")
        book = get_object_or_404(Book, id=book_id)
        return Copy.objects.filter(book__id=book_id)


def get_return_date():
    actual_date = datetime.date.today()
    return_date = actual_date + datetime.timedelta(days=5)
    if return_date.weekday() >= 5:
        until_monday = 7 - return_date.weekday()
        return_date += datetime.timedelta(days=until_monday)
    return datetime.datetime.combine(return_date, datetime.datetime.min.time())


class LoanView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, IsEmployeeOrReadOnly]
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer

    def perform_create(self, serializer):
        book_id = self.kwargs.get("book_id")
        book = get_object_or_404(Book, id=book_id)
        user = get_object_or_404(User, username=self.request.data["username"])
        copy = Copy.objects.filter(book__id=book_id, status=False)
        if copy:
            serializer.save(return_date=get_return_date(), copy=copy[0], user=user)
            CopySerializer(copy[0])
            copy[0].status = True
            copy[0].save()
        else:
            raise ValueError("all books are borrowed")


class ReturnView(generics.UpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer

    def update(self, request, *args, **kwargs):
        loan_id = self.kwargs.get("loan_id")
        loan = get_object_or_404(Loan, id=loan_id)
        if loan.returned:
            return HttpResponse({"message": "Book already returned"})
        copy = Copy.objects.get(id=loan.copy.id)
        CopySerializer(copy)
        copy.status = False
        copy.save()
        loan.returned = True
        loan.save()
        return HttpResponse({"message": "Successfully returned book"})
