import json

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model

from app_main.models import Note
from .serializers import NoteSerializer, UserSerializer

User = get_user_model()


@api_view(['GET'])
def get_notes(request):
    notes = Note.objects.all()  # QuerySet[<Note object>, ...]
    serialized_data = NoteSerializer(instance=notes, many=True)
    return Response(data=serialized_data.data)


@api_view(['GET'])
def get_users(request):
    users = User.objects.all()
    serialized_data = UserSerializer(
        instance=users, many=True)
    return Response(data=serialized_data.data)


@api_view(['POST'])
def create_note(request):
    if request.method == 'POST':
        owner_id = request.data.get('owner')
        title = request.data.get('title')
        body = request.data.get('body')

        errors = []

        if not owner_id:
            errors.append({"owner": "Note should have an owner"})

        if not title:
            errors.append({"title": "Note should have a title"})

        if errors:
            return Response(data=json.dumps(errors), status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.get(id=owner_id)
        note = Note.objects.create(owner=user, title=title, body=body)
        note.save()
        return Response(data="Created", status=status.HTTP_201_CREATED)

    return Response()


@api_view(['POST'])
def create_user(request):
    if request.method == 'POST':
        user_id = request.data['user']
        email = request.data['email']
        username = request.data['username']
        last_name = request.data['last_name']
        first_name = request.data['first_name']
        password = request.data['password']

        user = User.objects.get(id=user_id)
        user = User.objects.create(email=email, username=username, last_name=last_name, 
                                   first_name=first_name, password=password)
        user.save()
        return Response(data="Created", status=status.HTTP_201_CREATED)

    return Response()


@api_view(['GET', 'PATCH', 'DELETE'])
def note_detail(request, id):
    try:
        note = Note.objects.get(id=id)
    except:
        note = None

    if not note:
        return Response(data={"detail": "No such note with this ID"})

    if request.method == 'GET':
        note = NoteSerializer(instance=note, many=False).data
        return Response(data=note)

    elif request.method == 'PATCH':
        title = request.data.get('title') or None
        body = request.data.get('body') or None

        if title:
            note.title = title

        if body:
            note.body = body

        note.save()
        note = NoteSerializer(instance=note, many=False).data

        return Response(data=note)

    elif request.method == 'DELETE':
        note.delete()
        return Response(data='Deleted', status=status.HTTP_204_NO_CONTENT)
    

@api_view(['GET', 'PATCH', 'DELETE'])
def user_detail(request, id):
    try:
        user = User.objects.get(id=id)
    except:
        user = None

    if not user:
        return Response(data={"detail": "No such user with this ID"})

    if request.method == 'GET':
        user = UserSerializer(instance=user, many=False).data
        return Response(data=user)

    elif request.method == 'PATCH':
        email = request.data.get('email') or None
        username = request.data.get('username') or None
        last_name = request.data.get('last_name') or None
        first_name = request.data.get('first_name') or None
        password = request.data.get('password') or None

        if email:
            user.email = email

        if username:
            user.username = username

        if last_name:
            user.last_name = last_name

        if first_name:
            user.first_name = first_name

        if password:
            user.password = password

        user.save()
        user = UserSerializer(instance=user, many=False).data

        return Response(data=user)

    elif request.method == 'DELETE':
        user.delete()
        return Response(data='Deleted', status=status.HTTP_204_NO_CONTENT)