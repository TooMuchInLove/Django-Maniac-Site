from django.urls import path
from . import views

urlpatterns = [
    path('search-info/', views.search_info, name='search'),
    path('', views.list_category, name='list-category'),
    path('<int:id>/list-elements/', views.list_elements, name='list-elements'),
    path('<int:id>/list-elements/get-rating', views.get_rating, name='get-rating'),
    path('<int:id>/list-elements/info-element', views.info_element, name='info-element'),
]