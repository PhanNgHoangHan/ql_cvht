from django.urls import path
from .views import dashboard

urlpatterns = [
    path('dashboard/', dashboard, name='cv_dashboard'),
]
