from django.contrib import admin
from django.urls import path,include
from . import views, form_creator, form_editor

urlpatterns = [
    # path('', views.article_list, name='index-media'),
    # path('<str:id_sec>/', views.article_list),

    #Просмотр статей
    path('news/<str:id_news>/', views.news_detail, name='news-media'),
    path('section/<str:id_sec>/detail/<str:id_art>/', views.article_detail, name='detail-media'),
    path('section/<str:id_sec>/tag/<str:id_tag>/', views.article_list, name='index-media'),
    path('page_not_found/', views.page_not_found, name="page-not-found"),

    # Для редактирования старой статьи
    path('publish/<str:id_project>', form_creator.mediaform, name='form-publish'),  # Для публикации новой статьи
    path('post/<str:id_project>', form_creator.post, name='form-post'),

    # Для редактирования старой статьи
    path('project/<str:id_project>/edit/<str:id_article>', form_editor.mediaform_editor, name='form-edit'),
    path('project/<str:id_project>/edit-post/<int:id_article>', form_editor.post_edit, name='form-edit-post'),
]