from django.urls import path

from . import views


urlpatterns = [
    path("loans/<int:book_id>/", views.LoanView.as_view()),
    path("returns/<int:loan_id>/", views.ReturnView.as_view()),
]
