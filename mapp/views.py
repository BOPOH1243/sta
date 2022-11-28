from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import permissions
from .models import *
from .serializers import *
# Create your views here.
import json


class LevelViewset(viewsets.ModelViewSet):
    queryset = Level.objects.all()
    serializer_class = LevelSerializer


class PerevalViewset(viewsets.ModelViewSet):
    queryset = Pereval.objects.all()
    serializer_class = PerevalSerializer


class UserViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ImageViewset(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer


class AreaViewset(viewsets.ModelViewSet):
    queryset = Area.objects.all()
    serializer_class = AreaSerializer



class CoordsViewset(viewsets.ModelViewSet):
    queryset = Coords.objects.all()
    serializer_class = CoordsSerializer

#FIXME добавить все вьюсеты

def submitData(request):
    if request.method == 'POST':
        json_params = json.loads(request.body)
        json_data = json_params
        Pereval.objects.create(
            beauty_title=json_data['beauty_title'],
            title=json_data['title'],
            user=User.objects.get(email=json_data['user']['email']) if User.objects.get(email=json_data['user']['email']) else User.objects.create(
                email=json_data['user']['email'],
                name=json_data['user']['name'],
                family_name=json_data['user']['fam'],
                patronymic=json_data['user']['otc'],
                phone=json_data['user']['phone'],
            ),
            coords=Coords.objects.create(
                latitude=json_data['coords']['latitude'],
                longitude=json_data['coords']['longitude'],
                height=json_data['coords']['height'],
            ),
            level=Level.objects.create(
                winter=json_data['level']['winter'] if json_data['level']['winter'] else None,
                summer=json_data['level']['summer'] if json_data['level']['summer'] else None,
                autumn=json_data['level']['autumn'] if json_data['level']['autumn'] else None,
                spring=json_data['level']['spring'] if json_data['level']['spring'] else None,
            ),
            images=[Image.objects.create(title=raw_image['title'], image=raw_image['data']) for raw_image in json_data['images']],
        )
