from django.urls import path

from . import views
from copies.views import CopyView

urlpatterns = [
    path("books/", views.BookView.as_view()),
    path("books/<int:book_id>/copies/", CopyView.as_view()),
]
