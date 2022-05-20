from django.urls import path
from . import views

urlpatterns = [
    path('', views.shot_create),
    path('shots/<int:page>', views.shots),
    path('<int:shot_id>/', views.shot_detail_or_update_or_delete),
    path('<int:shot_id>/likes/', views.shot_likes),
    path('<int:shot_id>/comments/', views.shot_comment_create),
    path('<int:shot_id>/comments/<int:comment_id>/', views.shot_comment_update_or_delete),
]
