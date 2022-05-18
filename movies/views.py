from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Movie


# TMDB 로부터 movie data 가져올 때 사용하는 함수
# python manage.py migrate 후 다음 함수 실행되어야 에러가 나지 않는다.
# from . import dump_movie_data
# dump_movie_data.get_movie_data()


@api_view(['GET'])
def movie_popular(request):
    '''
    인기 영화 상위 10개를 리턴하는 API

    ---
    - order_by('-popularity')
    '''
    movies = list(Movie.objects.all().order_by('-popularity')[:10].values())
    data = {
        "movies" : movies,
    }
    return Response(data)