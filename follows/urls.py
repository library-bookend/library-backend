from django.urls import path
from .views import FollowView, FollowDetailView

urlpatterns = [
    path("follows/", FollowView.as_view()),
    path("follows/<int:book_id>/", FollowDetailView.as_view()),
]
