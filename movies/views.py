from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .serailizers import MovieListSerializer, MovieSerializer, MovieCommentSerializer, StarSerializer
from .models import Movie, MovieComment, StarRating
from django.db.models import Count
import random


# TMDB 로부터 movie data 가져올 때 사용하는 함수
# python manage.py migrate 후 다음 함수 실행되어야 에러가 나지 않는다.
# from . import dump_movie_data
# dump_movie_data.get_movie_data()

MOVIE_NUM = 10

@api_view(['GET'])
def movie_trailer(request):
    '''
    movie_trailer

    ---
    최신 상영작 중 랜덤한 movie_trailer 를 리턴하는 API
    '''
    # movies = Movie.objects.all() \
    #             .annotate(video_cnt=Count('video')) \
    #             .order_by('-release_date','-video_cnt')[:20]
    movies = Movie.objects.all().order_by('-release_date')[:20]
    serializers = MovieSerializer(movies, many=True)
    movies = serializers.data
    video_urls = []
    for movie in movies:
        if movie['video']: # 비디오 정보가 있는 경우 리스트에 video key 값을 append
            for video in movie['video']:
                video_urls.append(video['key'])
    data = {
        'trailer' : 'https://www.youtube.com/embed/' + random.sample(video_urls,1)[0]
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
    # movies = list(Movie.objects.all().order_by('-popularity')[:20].values())
    movies = Movie.objects.all().order_by('-popularity')
    max_page = round(len(movies)/MOVIE_NUM)
    page -= 1
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
    movies = Movie.objects.all().order_by('-release_date')
    max_page = round(len(movies)/MOVIE_NUM)
    page -= 1
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

    stars = ''
    if movie.stars.filter(user=request.user).exists():
        stars = list(movie.stars.values())[0]
    
    serializer = MovieSerializer(movie)
    data = {
        "stars" : stars,
        "movie" : serializer.data,
    }
    return Response(data)


@api_view(['POST'])
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
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['PUT', 'DELETE'])
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
            return Response(serializer.data)

    def comment_delete():
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    if request.method == 'PUT':
        return comment_update()
    elif request.method == 'DELETE':
        return comment_delete()


@api_view(['POST', 'DELETE'])
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