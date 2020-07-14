from django.urls import path
from blog import api

urlpatterns = [
    path('add-article/',api.add_article)
    
]