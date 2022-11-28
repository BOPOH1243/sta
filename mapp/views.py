from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import permissions
from .models import *
from .serializers import *
# Create your views here.


class LevelViewset(viewsets.ModelViewSet):
    queryset = Level.objects.all()
    serializer_class = LevelSerializer


class PerevalViewset(viewsets.ModelViewSet):
    queryset = Pereval.objects.all()
    serializer_class = PerevalSerializer

#FIXME добавить все вьюсеты