from django.urls import path
from .views import  LoginApiView, RegistrationApiView

urlpatterns = [
    path('register/', RegistrationApiView.as_view(), name='register'),
    path('login/', LoginApiView.as_view(), name="login"),
    
]