from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from apps.compliance_core.utils import ComplianceChecker

class CampaignImageUploadView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
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
        image = request.FILES.get('image')
        if not image:
            return Response({'error': 'An image must be sent'}, status=status.HTTP_400_BAD_REQUEST)
        
        api_key = request.data.get('api_key')
        if not api_key:
            return Response({'error': 'An API key must be provided'}, status=status.HTTP_400_BAD_REQUEST)

        # Call compliance_core to process the image
        compliance_checker = ComplianceChecker(api_key)
        data = {
            'image': image,
        }
        campaign_result = compliance_checker.verify_campaign(data)

        return Response({
            'message': 'Image received and processed correctly',
            'result': campaign_result,
        }, status=status.HTTP_200_OK)
