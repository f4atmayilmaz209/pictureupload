
import os
import uuid
import random
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

        ########################TASK-1#############################################################
        image_file = request.FILES.get("image")

        if not image_file:
            return Response(
                {"error": "No image provided"}, status=status.HTTP_400_BAD_REQUEST
            )

        # Resmi byte olarak oku
        image_bytes = np.frombuffer(image_file.read(), np.uint8)

        # OpenCV ile resmi oku
        img = cv2.imdecode(image_bytes, cv2.IMREAD_UNCHANGED)


        # Boyutları al
        height, width, channels = img.shape

        print(f"Genişlik: {width}px")
        print(f"Yükseklik: {height}px")
        print(f"Renk kanalı sayısı: {channels}")


        ########################TASK-2#############################################################
        # # 2. DİKDÖRTGEN çiz (sol üst ve sağ alt köşe)
        min_size = 50
        max_size = 200

        # 3. Rastgele sol üst köşe belirle (x1, y1)
        x1 = random.randint(0, width - min_size)
        y1 = random.randint(0, height - min_size)

        # 4. Rastgele genişlik ve yükseklik belirle, sınırları aşmasın
        rect_width = random.randint(min_size, min(max_size, width - x1))
        rect_height = random.randint(min_size, min(max_size, height - y1))

        # 5. Sağ alt köşeyi hesapla
        x2 = x1 + rect_width
        y2 = y1 + rect_height

        # 6. Renk ve kalınlık
        color = (0, 255, 0)  # Yeşil
        thickness = 2

        # 7. Dikdörtgen çiz
        cv2.rectangle(img, (x1, y1), (x2, y2), color, thickness)

        # 3. DAİRE çiz (merkez, yarıçap)
        max_radius = min(width, height) // 4  # sınırı aşmaması için oranla
        radius = random.randint(10, max_radius)

        # 3. Merkez noktasını sınır içinde rastgele belirle
        cx = random.randint(radius, width - radius)
        cy = random.randint(radius, height - radius)
        center = (cx, cy)

        # 4. Renk ve kalınlık
        color = (0, 0, 255)  # Yeşil
        thickness = 3

        # 5. Daire çiz
        cv2.circle(img, center, radius, color, thickness)

        # # 4. ÇİZGİ çiz (başlangıç - bitiş)
        # 2. Başlangıç noktası (x1, y1) rastgele, görüntü boyutu içinde
        x1 = random.randint(0, width - 1)
        y1 = random.randint(0, height - 1)

        # 3. Bitiş noktası (x2, y2) rastgele, görüntü boyutu içinde
        x2 = random.randint(0, width - 1)
        y2 = random.randint(0, height - 1)

        # 4. Renk ve kalınlık
        color = (0, 0, 255)  # Kırmızı (BGR)
        thickness = 2

        # 5. Çizgi çiz
        cv2.line(img, (x1, y1), (x2, y2), color, thickness)

        # 6. Görüntüyü göster
        cv2.imwrite("Geometrik Sekiller.jpg", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


        
        #$$$$RGB Kanalları 3 farklı görüntü$$$$#

        # 2. Kanalları ayır (OpenCV -> BGR formatındadır)
        B, G, R = cv2.split(img)

        # 3. Her bir kanal tek başına gri tonlu görseldir
        #    Bunları ayrı dosyalar olarak kaydedebiliriz:
        cv2.imwrite("blue_channel.jpg", B)
        cv2.imwrite("green_channel.jpg", G)
        cv2.imwrite("red_channel.jpg", R)

        # 4. İsteğe bağlı: her kanalı sahte renkli görüntü olarak göster (tek kanal -> 3 kanal)
        blue_img = cv2.merge([B, B*0, B*0])    # B, 0, 0
        green_img = cv2.merge([G*0, G, G*0])   # 0, G, 0
        red_img = cv2.merge([R*0, R*0, R])     # 0, 0, R

        cv2.imwrite("blue_visual.jpg", blue_img)
        cv2.imwrite("green_visual.jpg", green_img)
        cv2.imwrite("red_visual.jpg", red_img)

        print("✅ RGB (BGR) kanalları ayrı ayrı kaydedildi.")

        #$$$$BGR-RGB-Grayscale$$$$#
        rgb_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # 3. RGB → Grayscale dönüşümü
        gray_image = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2GRAY)

        # 4. Görselleri kaydet
        cv2.imwrite("01_bgr_input.jpg", img)
        cv2.imwrite("02_rgb_converted.jpg", rgb_image)
        cv2.imwrite("03_grayscale_from_rgb.jpg", gray_image)


        #$$$$$EDGE DETECTION#####$$$$$
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # 2. Gürültüyü azaltmak için Gaussian blur uygula
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        # 3. Canny kenar tespiti uygula
        edges = cv2.Canny(blurred, threshold1=100, threshold2=200)

        # 4. Sonuçları kaydet
        cv2.imwrite("01_gray.jpg", gray)
        cv2.imwrite("02_blurred.jpg", blurred)
        cv2.imwrite("03_edges.jpg", edges)

        # 5. İsteğe bağlı: göster
        cv2.imwrite("Canny Edge Detection.jpg", edges)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

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
