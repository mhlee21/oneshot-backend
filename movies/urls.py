from django.urls import path
from . import views


urlpatterns = [
    path('movie_trailer/', views.movie_trailer),
    path('popular/<int:page>/', views.movie_popular),
    path('now_playing/<int:page>/', views.now_playing),
    path('<int:movie_id>/', views.movie_detail),
    path('<int:movie_id>/likes/', views.movie_likes),
    path('<int:movie_id>/comments/', views.movie_comment_create),
    path('<int:movie_id>/comments/<int:comment_id>/', views.movie_update_or_delete),
    path('<int:movie_id>/star_rating/', views.movie_star_rating),
    # path('<int:movie_id>/star_rating/<int:star_id>/', views.movie_star_rating_update_or_delete),
]
