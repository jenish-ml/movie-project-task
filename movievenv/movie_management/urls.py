from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add_movie/', views.add_movie, name='add_movie'),
    path('movie/<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('movie/<int:movie_id>/edit/', views.edit_movie, name='edit_movie'),
    path('movie/<int:movie_id>/delete/', views.delete_movie, name='delete_movie'),
    path('movie/<int:movie_id>/add_review/', views.add_review, name='add_review'),
]

