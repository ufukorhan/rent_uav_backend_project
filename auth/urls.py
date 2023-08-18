from django.urls import path
from auth.views import AuthView


urlpatterns = [
    path("login/", AuthView.as_view(), name="login"),
]
