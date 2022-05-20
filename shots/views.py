from xml.etree.ElementTree import Comment
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Shot, ShotComment
from movies.models import Movie
from .serializers.shot import ShotSerializer, ShotListSerializer
from .serializers.shot_comment import ShotCommentSerializer
from django.db.models import Count

@api_view(['GET', 'POST'])
def shots(request):
    '''
    shots

    ---
    [GET] get shots

    [POST] create shots
    * title
    * content
    * movie_char
    * image
    '''
    def shot_list():
        shots = Shot.objects.all().annotate(like_cnt=Count('like_users')).order_by('-like_cnt', '-pk')
        serializer = ShotListSerializer(shots, many=True)
        return Response(serializer.data)

    def shot_create():
        serializer = ShotSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    if request.method == 'GET':
        return shot_list()
    elif request.method == 'POST':
        return shot_create()


@api_view(['GET', 'PUT', 'DELETE'])
def shot_detail_or_update_or_delete(request, shot_id):
    '''
    shot_detail_or_update_or_delete

    ---
    [GET] 

    [PUT] 
    - title
    - content
    - image

    [DELETE]
    - title
    -content
    - image (수정시에도 image 넣어줘야함) 
    '''
    shot = get_object_or_404(Shot, pk=shot_id)

    def shot_detail():
        serializer = ShotSerializer(shot)
        return Response(serializer.data)

    def shot_update():
        if request.user == shot.user:
            serializer = ShotSerializer(instance=shot, data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
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


@api_view(['POST'])
def likes(request, shot_id):
    '''
    likes

    ---
    [POST]

    return { "is_like": true, "like_cnt": 1 }
    '''
    shot = get_object_or_404(Shot, pk=shot_id)
    if shot.like_users.filter(pk=request.user.pk).exists():
        shot.like_users.remove(request.user)
        is_like = False
    else:
        shot.like_users.add(request.user)
        is_like = True
    data = {
        'is_like': is_like,
        'like_cnt': shot.like_users.count()
    }
    return Response(data)


@api_view(['POST'])
def comment_create(request, shot_id):
    '''
    comment_create

    ---
    [POST]
    * content
    '''
    shot = get_object_or_404(Shot, pk=shot_id)
    serializer = ShotCommentSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(shot=shot, user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['PUT', 'DELETE'])
def comment_update_or_delete(request, shot_id, comment_id):
    '''
    comment_update_or_delete

    ---
    [PUT]
    * content

    [DELETE]
    '''
    comment = get_object_or_404(ShotComment, pk=comment_id)
    
    def comment_update():
        serializer = ShotCommentSerializer(comment, request.data)
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