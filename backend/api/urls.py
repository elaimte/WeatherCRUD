

from django.urls import path
from .views import UserRegistrationView, UserLoginView, WeatherView, DashboardView, autocomplete_city

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('weather/<str:city_name>/', WeatherView.as_view(), name='weather'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('autocomplete-city/', autocomplete_city, name='autocomplete_city'),
    
]
