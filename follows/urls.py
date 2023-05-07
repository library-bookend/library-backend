from django.urls import path
from .views import FollowDetailView

urlpatterns = [
    path('books/<int:pk>/follows/', FollowDetailView.as_view()),
]
