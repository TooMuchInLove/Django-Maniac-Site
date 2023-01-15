from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index-catalog'),
    path('genres_list/<int:pk>/', views.genre_detail_view, name='genre-detail'),
    path('artists_list/<int:pk>/', views.artist_detail_view, name='artist-card'),
]
