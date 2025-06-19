from rest_framework import serializers
from .models import Campaign, CampaignImage


class CampaignImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CampaignImage
        fields = '__all__'

class CampaignSerializer(serializers.ModelSerializer):
    # Two options for sending the associated images:
    # 1. Using a nested serializer for CampaignImage
    # 2. Using a list of image IDs or URLs
    image_urls = serializers.SerializerMethodField()

    def get_image_urls(self, obj):
        request = self.context.get('request')
        if not request:
            return []
        urls = [request.build_absolute_uri(image.image.url) for image in obj.images.all()]
        return urls

    class Meta:
        model = Campaign
        fields = ['id', 'name', 'description', 'creation_date', 'update_date', 'status', 'reason', 'created_by', 'last_time_checked_by', 'image_urls']
        read_only_fields = ['id', 'creation_date', 'update_date']  # Campos que no se deberían crear/actualizar directamente
