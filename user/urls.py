from django.urls import path
from . import views

urlpatterns = [
    path("registration/", views.registration_api_view),
    path("authorization/", views.autorization_api_view),
    path("confirm/", views.confirm_api_view),
]
