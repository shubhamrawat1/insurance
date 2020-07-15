from django.urls import path
from .views import *

urlpatterns = [
    path('insurance-finder/', InsuranceFinder.as_view(), name='insurance'),
]






