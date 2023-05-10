from django.urls import path
from .views import RatingsDetailView

urlpatterns = [
    path('books/<int:pk>/ratings/', RatingsDetailView.as_view()),
]
