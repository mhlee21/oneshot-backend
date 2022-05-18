from django.urls import path
from . import views
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

urlpatterns = [
    path('movie/popular/', views.movie_popular),
]
