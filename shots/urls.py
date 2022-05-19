from django.urls import path
from . import views

urlpatterns = [
    path('', views.shots),
    path('<int:shot_id>/', views.shot_detail_or_update_or_delete),
    path('<int:shot_id>/likes/', views.likes),
    path('<int:shot_id>/comments/', views.comment_create),
    path('<int:shot_id>/comments/<int:comment_id>/', views.comment_update_or_delete),
]
