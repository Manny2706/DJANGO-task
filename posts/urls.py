from django.urls import path
from . import views


urlpatterns = [
	path('', views.home, name='home'),
	path('post/<int:pk>/', views.post_detail, name='post_detail'),
	path('post/new/', views.create_post, name='create_post'),
	path('post/<int:pk>/edit/', views.update_post, name='update_post'),
	path('post/<int:pk>/delete/', views.delete_post, name='delete_post'),
]


