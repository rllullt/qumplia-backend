from django.urls import path
from .views import CampaignImageUploadView

urlpatterns = [
    path('new/', CampaignImageUploadView.as_view(), name='campaign-image-upload'),
]
