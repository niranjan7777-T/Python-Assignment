
from django.urls import path,include
from .views import *



urlpatterns = [
    path('joke', JokeAPI.as_view()),  # Include the URLs of the second app
    path('upload-excel',UploadExcel.as_view())
]

