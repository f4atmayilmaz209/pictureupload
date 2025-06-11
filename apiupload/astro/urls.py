from django.urls import path 
from .views import ImageConvertView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('uploadpicture/',ImageConvertView.as_view(),name='convert-image'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)