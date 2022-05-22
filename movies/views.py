from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serailizers import GenreSerializer, MovieListSerializer, MovieSerializer, MovieCommentSerializer, StarSerializer
from .models import Movie, MovieComment, StarRating, Genre
from django.db.models import Count
import random
import datetime as dt

# TMDB 로부터 movie data 가져올 때 사용하는 함수
# python manage.py migrate 후 다음 함수 실행되어야 에러가 나지 않는다.
# from . import dump_movie_data
# dump_movie_data.get_movie_data()

MOVIE_NUM = 12

@api_view(['GET'])
def genre(request):
    '''
    genre

    ---
    [GET]
    '''
    genres = get_list_or_404(Genre)
    serializer = GenreSerializer(genres, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def movie_trailer(request):
    '''
    movie_trailer

    ---
    최신 상영작 중 랜덤한 movie_trailer 를 리턴하는 API
    '''
    today = dt.datetime.now()
    start = today - dt.timedelta(30)
    end = today + dt.timedelta(30)
    movies = Movie.objects.all().order_by('-release_date')\
        .filter(release_date__range=(start, end))[:20]
    serializer = MovieSerializer(movies, many=True)
    movies = []
    for movie in serializer.data:
        if movie['video']: # 비디오 정보가 있는 경우 리스트에 video key 값을 append
            movies.append(movie)
    movie = random.sample(movies,1)[0]
    trailer = 'https://www.youtube.com/embed/' + movie['video'][0]['key']
    data = {
        'movie': movie,
        'trailer' : trailer,
    }
    return Response(data)


@api_view(['GET'])
def movie_popular(request, page):
    '''
    movie_popular

    ---
    - order_by('-popularity')

    페이지 번호에 따라 인기영화 상위 20개씩 반환하는 API
    
    max_page를 넘어가는 값을 page 로 주면 빈 리스트를 반환합니다.
    '''
    movies = Movie.objects.all().order_by('-popularity')
    max_page = round(len(movies)/MOVIE_NUM)

    movies = movies[page*MOVIE_NUM:page*MOVIE_NUM+MOVIE_NUM]
    serializer = MovieListSerializer(movies, many=True)
    data = {
        "max_page"  : max_page,
        "movie_cnt" : MOVIE_NUM,
        "movies"    : serializer.data,
    }
    return Response(data)


@api_view(['GET'])
def now_playing(request, page):
    '''
    now_playing

    ---
    - order_by('-popularity')

    페이지 번호에 따라 최신 상영작 20개씩 반환하는 API
    
    max_page를 넘어가는 값을 page 로 주면 빈 리스트를 반환합니다.
    '''
    today = dt.datetime.now()
    start = today - dt.timedelta(30)
    end = today + dt.timedelta(30)
    movies = Movie.objects.all().order_by('-release_date')\
        .filter(release_date__range=(start, end))
    max_page = round(len(movies)/MOVIE_NUM)

    movies = movies[page*MOVIE_NUM:page*MOVIE_NUM+MOVIE_NUM]
    serializer = MovieListSerializer(movies, many=True)
    data = {
        "max_page"  : max_page, 
        "movie_cnt" : MOVIE_NUM,
        "movies"    : serializer.data,
    }
    return Response(data)


@api_view(['GET'])
def movie_detail(request, movie_id):
    '''
    movie_detail

    ---
    [GET] 영화 상세 정보

    * stars: 현재 접속중인 유저의 별점 평가 내역 있으면 같이 리턴, 없으면 ''를 리턴
    * movie : 영화 상세 정보
    '''
    movie = get_object_or_404(Movie, pk=movie_id)

    # 별점 정보
    stars = ''
    # AnonymousUser 에러 해결을 위해 
    # request.user.id 값이 있는지 없는지를 검사
    # AnonymousUser 일때 id 값이 None 이기 때문에 TypeError 발생
    if request.user.id:
        if movie.stars.filter(user=request.user).exists():
            stars = list(movie.stars.values())[0]

    # 영화 포스터/트레일러 url
    url_path = ''
    if movie.video.values(): 
        key = list(movie.video.values())[0]['key']
        url_path = f'https://www.youtube.com/embed/{key}'
    else:
        url_path = f'https://image.tmdb.org/t/p/original{movie.poster_path}'
    
    serializer = MovieSerializer(movie)
    data = {
        "url_path" : url_path,
        "stars" : stars,
        "movie" : serializer.data,
    }
    return Response(data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def movie_likes(request, movie_id):
    '''
    movie_likes

    ---
    [POST]
    '''
    movie = get_object_or_404(Movie, pk=movie_id)
    if movie.like_users.filter(pk=request.user.pk).exists():
        movie.like_users.remove(request.user)
        is_like = False
    else:
        movie.like_users.add(request.user)
        is_like = True
    data = {
        'is_like': is_like,
        'like_cnt': movie.like_users.count()
    }
    return Response(data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def movie_comment_create(request, movie_id):
    '''
    movie_comment_create

    ---
    [POST]
    '''
    movie = get_object_or_404(Movie, pk=movie_id)
    serializer = MovieCommentSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(movie=movie, user=request.user)
        res = MovieSerializer(movie)
        return Response(res.data['comments'], status=status.HTTP_201_CREATED)


@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def movie_update_or_delete(request, movie_id, comment_id):
    '''
    movie_update_or_delete

    ---
    [PUT]

    * content

    [DELETE]
    '''
    comment = get_object_or_404(MovieComment, pk=comment_id)
    
    def comment_update():
        serializer = MovieCommentSerializer(comment, request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            movie = get_object_or_404(Movie, pk=movie_id)
            res = MovieSerializer(movie)
            return Response(res.data['comments'])

    def comment_delete():
        comment.delete()
        movie = get_object_or_404(Movie, pk=movie_id)
        res = MovieSerializer(movie)
        return Response(res.data['comments'])

    if request.method == 'PUT':
        return comment_update()
    elif request.method == 'DELETE':
        return comment_delete()


@api_view(['POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def movie_star_rating(request, movie_id):
    '''
    movie_star_rating

    ---
    [POST]

    * 별점 생성, 수정 시 사용
    
    [DELETE]
    
    * 별점 삭제
    '''
    movie = get_object_or_404(Movie, pk=movie_id)

    def star_update():
        if movie.stars.filter(user=request.user):
            existed_star = list(movie.stars.filter(user=request.user).values())[0]
            star_id = existed_star['id']
            star = get_object_or_404(StarRating, pk=star_id)
            serializer = StarSerializer(star, request.data)
        else:
            serializer = StarSerializer(data=request.data)
        
        if serializer.is_valid(raise_exception=True):
            serializer.save(movie=movie, user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def star_delete():
        if movie.stars.filter(user=request.user):
            star = movie.stars.filter(user=request.user)
            star.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    if request.method == 'POST':
        return star_update()
    elif request.method == 'DELETE':
        return star_delete()