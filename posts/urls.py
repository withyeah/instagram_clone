# posts/urls.py
from django.urls import path
from . import views

app_name = 'posts'
urlpatterns = [
    path('<int:post_pk>/delete/', views.delete, name='delete'),
    path('<int:post_pk>/update/', views.update, name='update'),
    path('', views.list, name='list'),
    path('create/', views.create, name='create'),
]