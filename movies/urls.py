from django.urls import path
from . import views
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="ONESHOT API",
      default_version='v1',
      description="ONESHOT API description",
   ),
   public=True,
)

urlpatterns = [
    path('movie/popular/', views.movie_popular),
    path('swagger/', schema_view.with_ui('redoc')),
]
