from django.contrib import admin
from django.urls import (
    path
)
from app1.views import (
    SignUpAPIView,
    SignInAPIView,
    SignOutAPIView
)

urlpatterns = [
    path('signup/', SignUpAPIView.as_view()),
    path('signin/', SignInAPIView.as_view()),
    path('signout/', SignOutAPIView.as_view())
]