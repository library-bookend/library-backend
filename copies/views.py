from django.shortcuts import render, get_object_or_404
import datetime
from .models import Copy, Loan
from books.models import Book
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import generics
from rest_framework.views import Response
from library_bookend.permissions import IsEmployeeOrReadOnly
from django.http import HttpResponse
from .serializers import CopySerializer
from loans.serializers import LoanSerializer
from users.models import User
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.core.mail import send_mail
import os
import ipdb
import pytz


class CopyView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsEmployeeOrReadOnly]
    serializer_class = CopySerializer

    def get_queryset(self):
        book_id = self.kwargs.get("book_id")
        book = get_object_or_404(Book, id=book_id)
        copies = Copy.objects.filter(book__id=book_id)

        for copy in copies:
            loans = Loan.objects.filter(copy=copy)
            fine = sum(loan.fine for loan in loans)
            copy.fine = fine
            copy.save()

        return copies


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
            raise ValueError("all copies are borrowed")


class ReturnView(generics.UpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer

    def update(self, request, *args, **kwargs):
        now = datetime.datetime.now(datetime.timezone.utc)
        today = now.astimezone(pytz.utc).date()

        loan_id = self.kwargs.get("loan_id")
        loan = get_object_or_404(Loan, id=loan_id)

        if loan.returned:
            return Response({"message": "Book already returned"})
        copy = Copy.objects.get(id=loan.copy.id)
        CopySerializer(copy)
        copy.status = False
        copy.save()

        if loan.return_date.date() < today:
            delta = datetime.datetime.now() - loan.return_date
            fine = delta.days * 2
            loan.fine = fine
            loan.save()

        loan.returned = True
        loan.save()

        # users = User.objects.filter(
        #     following__book=loan.copy.book, following__status=True
        # )
        

        # for user in users:
        #     subject = f"Book Available: {loan.copy.book.title}"
        #     message = f"The book {loan.copy.book.title} is now available for loan at the library."
        #     from_email = os.environ.get(
        #         "EMAIL"
        #     )  # este projeto utiliza o email fornecido via venv por fins de testes e entrega, em um projeto real aqui iria o email da empresa
        #     to_email = [user.email]
        #     send_mail(subject, message, from_email, to_email, fail_silently=False)

        return Response({"message": "Successfully returned book"})
