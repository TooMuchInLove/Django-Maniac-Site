from django.urls import path,include
from . import views
from django.contrib.auth.views import LoginView, LogoutView, logout_then_login

urlpatterns = [
    # post views
    # path('login', views.user_login, name='login'),
    # path('logout-then-login/', logout_then_login, name='logout_then_login'),  # для чего?
    path('', views.dashboard, name='dashboard'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
    path('register/', views.register, name='register'),
    path('register/project', views.register_project, name='project-register'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/<int:pk>/', views.profile_view_pk, name='profile_pk'),
    # path('profile/<int:pk>/blog', views.profile_blog_view, name='profile-blog'),
    path('profile/<int:pk>/projects', views.profile_projects, name='profile_projects'),
    path('profile/edit', views.profile_edit, name='profile_edit'),
    path('profile/notifications', views.profile_notifications, name='profile_notifications'),
    path('profile/<int:pk>/subscriptions', views.profile_subscriptions, name='profile_subscriptions'),
    path('profile/answer_to_invite/<str:operation>/<int:pk>', views.answer_to_invite, name='answer_to_invite'),
    # path('profile/<int:pk>/subscriptions', views.user_subscriptions, name='user_subscriptions'),
    path('users_list', views.users_list, name='users-list'),
    path('profile/edit_password', views.password_edit, name='edit_password'),
    path('profile/project/<int:pk>/blog', views.project_blog, name='project_blog'),
    path('profile/project/<int:pk>/followers', views.project_followers, name='project_followers'),
    path('profile/project/<int:pk>/members', views.project_members, name='project_members'),
    path('profile/project/<int:pk>/edit', views.project_edit, name='project_edit'),
    path('profile/project/<int:pk>/add_member', views.add_member, name='add_member'),
    # path('subscribe/<str:operation>/<int:pk>', views.change_subscription, name='change_subscription') # работает
    path('subscribe/<str:operation>/<str:model>/<int:pk>', views.change_subscription, name='change_subscription'),
    # path('profile/project/<int:pk>/blog/<int:id_article>/article_edit', views.project_blog, name="article_edit"),  # Лексов
]
