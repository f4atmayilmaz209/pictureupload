import cv2
import numpy as np
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from django.http import HttpResponse
from django.core.files.base import ContentFile
import base64

class ImageConvertView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        image_file = request.FILES.get('image')

        if not image_file:
            return Response({'error': 'No image provided'}, status=status.HTTP_400_BAD_REQUEST)

        # Resmi byte olarak oku
        image_bytes = np.frombuffer(image_file.read(), np.uint8)


        # OpenCV ile resmi oku
        img = cv2.imdecode(image_bytes, cv2.IMREAD_UNCHANGED)

        if img is None:
            return Response({'error': 'Invalid image file'}, status=status.HTTP_400_BAD_REQUEST)

        # OpenCV ile PNG'ye dönüştür
        success, encoded_image = cv2.imencode('.png', img)
        if not success:
            return Response({'error': 'Could not convert to PNG'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Response olarak dön (Base64 veya raw image olarak)
        png_bytes = encoded_image.tobytes()

        # İstersen burada dosyayı kaydedebilirsin:
        with open('converted_image.png', 'wb') as f:
            f.write(png_bytes)

        # Raw PNG dosyasını response olarak gönder
        encoded = base64.b64encode(png_bytes).decode('utf-8')
        return Response({'image': encoded})
