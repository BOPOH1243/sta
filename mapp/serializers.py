from .models import *
from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField
import base64
import io
from django.core.files.images import ImageFile


class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = ('winter', 'summer', 'autumn', 'spring')


class PerevalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pereval
        fields = '__all__'
        depth = 1



class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = '__all__'


class CoordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coords
        fields = ('latitude', 'longitude', 'height')


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('image', 'title')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'phone', 'name', 'family_name', 'patronymic')
#
class ImageFuckedSerializer(serializers.Serializer):
    title = serializers.CharField()
    imagehex = serializers.CharField(max_length=20000000)
    def save(self, **kwargs):
        image_bytes = bytes.fromhex(self.validated_data['imagehex'])
        image = ImageFile(io.BytesIO(image_bytes), name=f'{self.validated_data["title"]}.jpg')  # << the answer!
        new_message = Image.objects.create(image=image, title=self.validated_data['title'])
        return new_message


class SubmitDataSerializer(serializers.ModelSerializer):
    coords = CoordsSerializer()
    level = LevelSerializer()
    user = UserSerializer()
    beauty_title = serializers.CharField()
    title = serializers.CharField()
    other_titles = serializers.CharField()
    class Meta:
        model = Pereval
        fields = ['coords', 'level', 'user', 'beauty_title', 'title', 'other_titles']

    def create(self, validated_data):
        coords = CoordsSerializer(data=validated_data['coords'])
        coords.is_valid()
        coords = coords.save()
        level = LevelSerializer(data=validated_data['level'])
        level.is_valid()
        level = level.save()
        user = UserSerializer(data=validated_data['user'])
        user.is_valid()
        user = user.save()
        beauty_title = validated_data['beauty_title']
        title = validated_data['title']
        other_titles=validated_data['other_titles']
        return Pereval.objects.create(
            coords=coords,
            level=level,
            user=user,
            beauty_title=beauty_title,
            title=title,
            other_titles=other_titles,
        )


