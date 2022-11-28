from .models import *
from rest_framework import serializers


class LevelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Level
        fields = '__all__'


class PerevalSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Pereval
        fields = '__all__'


class AreaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Area
        fields = '__all__'


class CoordsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Coords
        fields = '__all__'


class ImageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = '__all__'