from django.urls import path, include
from .views import RegistrationView, ActivationView, LoginView, LogoutView, ChangePasswordView, OwnerRequestCreateAPIView
from rest_framework.routers import DefaultRouter



urlpatterns = [
    path('registration/', RegistrationView.as_view()),
    path('activation/', ActivationView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('change_password/', ChangePasswordView.as_view()),
    path('owner/', OwnerRequestCreateAPIView.as_view())
]