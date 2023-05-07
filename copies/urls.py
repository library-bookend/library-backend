from django.urls import path

from . import views


urlpatterns = [
    path("loans/<uuid:book_id>/", views.LoanView.as_view()),
    path("returns/<uuid>book_id/", views.ReturnView.as_view())
]
