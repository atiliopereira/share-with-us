from django.urls import path
from uploads import views

urlpatterns = [
    path('', views.upload_file, name='upload_file'),
    path('gallery/', views.gallery, name='gallery'),
]