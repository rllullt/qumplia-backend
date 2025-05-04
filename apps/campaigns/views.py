from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status

class CampaignImageUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        """
        Upload an image for a campaign.
        The image is expected to be sent in the request body as a file upload.
        The image should be sent with the key 'image'.
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

        # Extract image metadata
        metadata = {
            'filename': image.name,
            'content_type': image.content_type,
            'size_bytes': image.size,
        }

        # For now, only answer that the image was received correctly
        return Response({
            'message': 'Image received correctly',
            'metadata': metadata,
        }, status=status.HTTP_200_OK)
