from django.urls import path
from . import views

urlpatterns = [
    path('', views.shots),
    path('<int:movie_id>/', views.shot_create),
    path('<int:movie_id>/<int:shot_id>/', views.shot_detail_or_update_or_delete),
]
