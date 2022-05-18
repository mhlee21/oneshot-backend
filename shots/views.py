from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Shot, ShotComment
from movies.models import Movie
from .serializers.shot import ShotSerializer, ShotListSerializer

@api_view(['GET'])
def shots(request):
    '''
    shots

    ---
    모든 shot 를 리턴하는 API
    '''
    shots = Shot.objects.all().order_by('-pk')
    serializer = ShotListSerializer(shots, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def shot_create(request, movie_id):
    '''
    shot_create

    ---
    shot 생성 API
    '''
    movie = get_object_or_404(Movie, pk=movie_id)
    serializer = ShotSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user, movie=movie)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def shot_detail_or_update_or_delete(request, movie_id, shot_id):
    '''
    shot_detail_or_update_or_delete

    ---
    [PUT] 
    - movie_id 바꿔서 넣어주는 것 금지! 
    - shot 의 movie 정보 바꾸고 싶으면 삭제 후 shot 재생성을 권장합니다.
    '''
    movie = get_object_or_404(Movie, pk=movie_id)
    shot = get_object_or_404(Shot, pk=shot_id)

    def shot_detail():
        serializer = ShotSerializer(shot)
        return Response(serializer.data)

    def shot_update():
        if request.user == shot.user:
            serializer = ShotSerializer(instance=shot, data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save(movie=movie)
                return Response(serializer.data)

    def shot_delete():
        if request.user == shot.user:
            shot.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    if request.method == 'GET':
        return shot_detail()
    elif request.method == 'PUT':
        return shot_update()
    elif request.method == 'DELETE':
        return shot_delete()

