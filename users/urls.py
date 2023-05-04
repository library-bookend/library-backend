from django.urls import path

from . import views

urlpatterns = [
    path("users/", views.UserView.as_view()),
    path("users/<int:user_id>/loans", views.UserLoansView.as_view()),
    path("login/", views.CustomLoginView.as_view()),
]
