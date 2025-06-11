
import os
import uuid

import cv2
import numpy as np
from django.conf import settings

from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView


class ImageConvertView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        image_file = request.FILES.get("image")

        if not image_file:
            return Response(
                {"error": "No image provided"}, status=status.HTTP_400_BAD_REQUEST
            )

        # Resmi byte olarak oku
        image_bytes = np.frombuffer(image_file.read(), np.uint8)

        # OpenCV ile resmi oku
        img = cv2.imdecode(image_bytes, cv2.IMREAD_UNCHANGED)

        # # if img is None:
        # #     return Response({'error': 'Invalid image file'}, status=status.HTTP_400_BAD_REQUEST)

        # # # OpenCV ile PNG'ye dönüştür
        # # success, encoded_image = cv2.imencode('.png', img)
        # # if not success:
        # #     return Response({'error': 'Could not convert to PNG'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # # # Response olarak dön (Base64 veya raw image olarak)
        # # png_bytes = encoded_image.tobytes()

        # # # İstersen burada dosyayı kaydedebilirsin:
        # # with open('converted_image.png', 'wb') as f:
        # #     f.write(png_bytes)
        ## Raw PNG dosyasını response olarak gönder
        # # encoded = base64.b64encode(png_bytes).decode('utf-8')
        # # return Response({'image': encoded})
        try:
            if img is None:
                return Response(
                    {"error": "Invalid image format."}, status=status.HTTP_400_BAD_REQUEST
                )

            # Benzersiz dosya ismi üret
            filename = f"{uuid.uuid4().hex}.png"
            filepath = os.path.join(settings.MEDIA_ROOT, filename)
        
            # PNG olarak kaydet
            saved = cv2.imwrite(filepath, img)

            if not saved:
                return Response(
                    {"error": "Image could not be saved."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
            # URL döndür
            file_url = request.build_absolute_uri(settings.MEDIA_URL + filename)
            return Response({"message": "Image saved successfully.", "image_url": file_url})
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
