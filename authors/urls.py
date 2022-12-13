from django.urls import path

from authors.views import AuthorRegisterView, login_create, login_view
from django.contrib.auth.views import (LogoutView)


app_name = "authors"

urlpatterns = [
    path("authors/login/", login_view, name="login"),
    path("authors/login/create/", login_create, name="login-create"),
    path("authors/register/", AuthorRegisterView.as_view(), name="register"),
    path("authors/logout/", LogoutView.as_view(), name="logout")
]
