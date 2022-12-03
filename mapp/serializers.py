from .models import *
from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField
import base64
import io
from django.core.files.images import ImageFile


class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = '__all__'


class PerevalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pereval
        fields = '__all__'
        depth = 1

    def create(self, validated_data):
        validated_data['status']='new'
        return super().create(validated_data)

class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = '__all__'


class CoordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coords
        fields = '__all__'


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('image', 'title')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'phone', 'name', 'family_name', 'patronymic')

    def is_valid(self, *, raise_exception=False):
        if User.objects.filter(email=self.initial_data.get('email')).exists():
            return True
        else:
            return super().is_valid(self, raise_exception=raise_exception)
    def save(self, **kwargs):
        user = User.objects.filter(email=self.validated_data.get('email'))
        if user.exists():
            return user.first()
        else:
            return User.objects.create(
                email=self.validated_data.get('email'),
                phone = self.validated_data.get('phone'),
                name= self.validated_data.get('name'),
                family_name= self.validated_data.get('family_name'),
                patronymic= self.validated_data.get('patronymic'),
            )

class SubmitDataSerializer(serializers.Serializer):
    beauty_title = serializers.CharField()
    title = serializers.CharField()
    other_titles = serializers.CharField()
    user = serializers.DictField()
    coords = serializers.DictField()
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()
    height = serializers.IntegerField()
    level = serializers.DictField()
    images = serializers.ListField()

class ImageFuckedSerializer(serializers.Serializer):
    title = serializers.CharField()
    imagehex = serializers.CharField(max_length=20000000)
    def save(self, **kwargs):
        image_bytes = bytes.fromhex(self.validated_data['imagehex'])
        image = ImageFile(io.BytesIO(image_bytes), name=f'foo.jpg')  # << the answer!
        new_message = Image.objects.create(image=image)
        return new_message



