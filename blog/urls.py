from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path('',mainpage, name='mainpage'),
    path('blog/',PostListView.as_view(), name='blog-home'),
    path('user/<str:username>',UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/',PostDetailView.as_view(), name='post-detail'),
    path('post/new/',PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/',PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/',PostDeleteView.as_view(), name='post-delete'),
    path('like/<int:pk>',like_post, name='like_post'),
    path('likes/',like_main_post, name='like_main_post'),
    path('create/comment/',add_comment, name='comments'),
]
