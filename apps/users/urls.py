from django.urls import path
from .views import UserViewSet, GroupViewSet

urlpatterns = [
    path('users/', UserViewSet.as_view(), name='user-list'),
]