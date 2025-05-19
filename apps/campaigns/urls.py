from django.urls import path, include
from rest_framework import routers
from .views import CampaignViewSet

router = routers.DefaultRouter()
router.register(r'', CampaignViewSet, basename='campaign')

urlpatterns = [
    path('', include(router.urls)),
]
