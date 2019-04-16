# posts/urls.py
from django.urls import path
from . import views

app_name = 'posts'
urlpatterns = [
    path('<int:post_pk>/like/', views.like, name='like'),
    path('<int:post_pk>/delete_comment/<int:comment_pk>/', views.delete_comment, name='delete_comment'),
    path('<int:post_pk>/create_comment/', views.create_comment, name='create_comment'),
    path('<int:post_pk>/delete/', views.delete, name='delete'),
    path('<int:post_pk>/update/', views.update, name='update'),
    path('', views.list, name='list'),
    path('create/', views.create, name='create'),
]