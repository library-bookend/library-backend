from django.urls import path
from . import views

urlpatterns = [
    path("loans/", views.LoanView.as_view()),
    path("loans/<int:loan_id>/", views.LoanDetailView.as_view()),
    ]
