from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from .models import Campaign, CampaignImage
from .serializers import CampaignSerializer
from apps.compliance_core.utils import ComplianceChecker


class CampaignViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows campaigns to be viewed or edited.
    """
    queryset = Campaign.objects.all().order_by('-creation_date')
    serializer_class = CampaignSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    # Overwrite the create method to handle the creation of campaigns
    def create(self, request, *args, **kwargs):
        """
        Upload an image for a campaign.
        The image is expected to be sent in the request body as a file upload.
        The image should be sent with the key 'image'.
        An API Key for LLM usage is required, with key 'api_key'.
        For now, the response will include metadata about the uploaded image.
        Test this endpoint:
            curl -X POST -F "image=@/path/to/image.jpg" http://localhost:8000/api/campaigns/new/
        or in YAAK:
            Method: POST
            Form Data: multipart/form-data
            Key: image
            Value: /path/to/image.jpg
        """
        print('Request:', request)
        print('Request data:', request.data)

        name = request.data.get('name')
        print('Name:', name)
        description = request.data.get('description')
        created_by = request.user  # El usuario autenticado con Simple JWT

        image = request.FILES.get('image')
        if not image:
            return Response({'error': 'An image must be sent'}, status=status.HTTP_400_BAD_REQUEST)
        
        api_key = request.data.get('apiKey')
        if not api_key:
            return Response({'error': 'An API key must be provided'}, status=status.HTTP_400_BAD_REQUEST)

        # Call compliance_core to process the image
        compliance_checker = ComplianceChecker(api_key)
        data = {
            'image': image,
        }
        campaign_result = compliance_checker.verify_campaign(data)

        new_campaign = Campaign(
            name=name,
            description=description,
            created_by=created_by,
            status=campaign_result.get('status', 'pending'),
            reason=campaign_result.get('reason', ''),
        )
        new_campaign.save()
        # Save the image to the campaign
        campaign_image = CampaignImage(
            campaign=new_campaign,
            image=image,
        )
        campaign_image.save()
        # Serialize the campaign
        serializer = CampaignSerializer(new_campaign)
        # Return the serialized data
        return Response({
            'message': 'Image received and processed correctly',
            'result': campaign_result,
            'campaign': serializer.data,
        }, status=status.HTTP_201_CREATED)
    
    # Example of another custom action (if more endpoints are needed)
    # @action(detail=True, methods=['post'])
    # def approve(self, request, pk=None):
    #     campaign = self.get_object()
    #     campaign.status = 'aprobada'
    #     campaign.save()
    #     serializer = self.get_serializer(campaign)
    #     return Response(serializer.data)
