from django.urls import path 
from .views import ImageConvertView

urlpatterns = [
    path('uploadpicture/',ImageConvertView.as_view(),name='convert-image'),

]