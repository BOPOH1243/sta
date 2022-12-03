from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import permissions
from .models import *
from django.http import HttpResponse
from .serializers import *
# Create your views here.
from rest_framework import status
import json
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
import io
from django.core.files.images import ImageFile


class LevelViewset(viewsets.ModelViewSet):
    queryset = Level.objects.all()
    serializer_class = LevelSerializer
    def update(self, request, pk, *args, **kwargs):
        level = self.queryset.get(pk=pk)
        pereval = Pereval.objects.filter(level=level)
        if pereval.exists():
            if pereval.first().status =='new':
                return super().update(request, *args, **kwargs)
            else:
                return HttpResponse(status=status.HTTP_403_FORBIDDEN)
        else:
            level.delete()
            return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PerevalViewset(viewsets.ModelViewSet):
    queryset = Pereval.objects.all()
    serializer_class = PerevalSerializer
    def update(self, request,pk, *args, **kwargs):
        if self.queryset.get(pk=pk).status =='new':
            return super().update(request,*args, **kwargs)
        else:
            return HttpResponse(status=status.HTTP_403_FORBIDDEN)
    def get_queryset(self):
        queryset = self.queryset
        user_id = self.request.query_params.get('user_id')
        user_email=self.request.query_params.get('user_email')
        if user_id is not None:
            user = User.objects.filter(pk=user_id)
            if user.exists():
                queryset = queryset.filter(user=user.first())
        if user_email is not None:
            user = User.objects.filter(email=user_email)
            if user.exists():
                queryset = queryset.filter(user=user.first())
        return queryset




class UserViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    def update(self, request, *args, **kwargs):
        return HttpResponse(status=status.HTTP_403_FORBIDDEN)


class ImageViewset(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    def update(self, request, pk, *args, **kwargs):
        image = self.queryset.get(pk=pk)
        pereval_image = PerevalImage.objects.filter(image=image)
        if pereval_image.exists():
            if pereval_image.first().pereval.status =='new':
                return super().update(request, *args, **kwargs)
            else:
                return HttpResponse(status=status.HTTP_403_FORBIDDEN)
        else:
            image.delete()
            return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AreaViewset(viewsets.ModelViewSet):
    queryset = Area.objects.all()
    serializer_class = AreaSerializer
    def update(self, request, pk, *args, **kwargs):
        area = self.queryset.get(pk=pk)
        pereval = Pereval.objects.filter(area=area)
        if pereval.exists():
            if pereval.first().status =='new':
                return super().update(request, *args, **kwargs)
            else:
                return HttpResponse(status=status.HTTP_403_FORBIDDEN)
        else:
            area.delete()
            return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CoordsViewset(viewsets.ModelViewSet):
    queryset = Coords.objects.all()
    serializer_class = CoordsSerializer
    def update(self, request, pk, *args, **kwargs):
        response_data = {
            'state': '0',
        }
        coords = self.queryset.get(pk=pk)
        pereval = Pereval.objects.filter(coords=coords)
        if pereval.exists():
            if pereval.first().status == 'new':
                response_data['state']='1'
                response_data['message']='success'
                update = super().update(request, *args, **kwargs)
                update.content = json.dumps(response_data)
                update.content_type="application/json"
                return update
            else:
                response_data['message']='pereval status is not *new*'
                return HttpResponse(json.dumps(response_data),status=status.HTTP_403_FORBIDDEN)
        else:
            coords.delete()
            response_data['message']='pereval does not exists that object was delete'
            return HttpResponse(json.dumps(response_data), content_type="application/json",status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
def fsubmitData(request):
    if request.method == 'POST':
        json_params = json.loads(request.body)
        json_data = json_params
        pereval = Pereval.objects.create(
            beauty_title=json_data.get('beauty_title'),
            title=json_data.get('title'),
            user=User.objects.get(email=json_data.get('user', {}).get('email')) if User.objects.filter(email=json_data.get('user', {}).get('email')).exists() else User.objects.create(
                email=json_data.get('user', {}).get('email'),
                name=json_data.get('user', {}).get('name'),
                family_name=json_data.get('user', {}).get('fam'),
                patronymic=json_data.get('user', {}).get('otc'),
                phone=json_data.get('user', {}).get('phone'),
            ),
            coords=Coords.objects.create(
                latitude=json_data.get('coords', {}).get('latitude'),
                longitude=json_data.get('coords', {}).get('longitude'),
                height=json_data.get('coords', {}).get('height'),
            ),
            level=Level.objects.create(
                winter=json_data.get('level', {}).get('winter') if json_data.get('level', {}).get('winter') else '',
                summer=json_data.get('level', {}).get('summer') if json_data.get('level', {}).get('summer') else '',
                autumn=json_data.get('level', {}).get('autumn') if json_data.get('level', {}).get('autumn') else '',
                spring=json_data.get('level', {}).get('spring') if json_data.get('level', {}).get('spring') else '',
            ),
            #images=[Image.objects.create(title=raw_image['title'], image=raw_image['data']) for raw_image in json_data['images']], # я бы так сделал, но джанго решил меня подставить
        )

        if pereval:
            pereval.images.set([Image.objects.create(title=raw_image.get('title'), image=raw_image.get('data')) for raw_image in json_data.get('images')],)
            pereval.save()

        response_data = {
            'id':pereval.pk
        }
        #return HttpResponse(PerevalSerializer(pereval).data)
        return HttpResponse(json.dumps(response_data), content_type="application/json", status=status.HTTP_201_CREATED, )
@csrf_exempt
def submitData(request):
    if request.method == 'POST':
        json_params = json.loads(request.body)
        json_data = json_params

        coords = CoordsSerializer(
            data={
                'latitude': json_data.get('coords', {}).get('latitude'),
                'longitude': json_data.get('coords', {}).get('longitude'),
                'height': json_data.get('coords', {}).get('height'),
            }
        )
        level = LevelSerializer(
            data={
                'winter': json_data.get('level', {}).get('winter') if json_data.get('level', {}).get('winter') else '',
                'summer': json_data.get('level', {}).get('summer') if json_data.get('level', {}).get('summer') else '',
                'autumn': json_data.get('level', {}).get('autumn') if json_data.get('level', {}).get('autumn') else '',
                'spring': json_data.get('level', {}).get('spring') if json_data.get('level', {}).get('spring') else '',
            }
        )
        images = [
            ImageFuckedSerializer(
                data={
                    'title': raw_image.get('title'),
                    'imagehex': raw_image.get('data'),
                }

            )
            for raw_image in json_data.get('images')
        ]
        user = UserSerializer(data={
            'email': json_data.get('user', {}).get('email'),
            'name': json_data.get('user', {}).get('name'),
            'family_name': json_data.get('user', {}).get('fam'),
            'patronymic': json_data.get('user', {}).get('otc'),
            'phone': json_data.get('user', {}).get('phone'),
        })
        if coords.is_valid()==False:
            return HttpResponse(json.dumps({'message':'coords is not valid'}), content_type="application/json", status=status.HTTP_400_BAD_REQUEST, )
        if level.is_valid()==False:
            return HttpResponse(json.dumps({'message':'level is not valid'}), content_type="application/json", status=status.status.HTTP_400_BAD_REQUEST, )
        for image in images:
            if image.is_valid() == False:
                return HttpResponse(json.dumps({'message': 'image is not valid'}), content_type="application/json", status=status.status.HTTP_400_BAD_REQUEST, )
        if user.is_valid()==False:
            user = User.objects.filter(email=json_data.get('user', {}).get('email'))
            if user.exists()==False:
                return HttpResponse(json.dumps({'message':'user is not valid'}), content_type="application/json", status=status.status.HTTP_400_BAD_REQUEST, )
            else: user=user.first()
        else:
            user = user.save()

        pereval = Pereval.objects.create(
            beauty_title=json_data.get('beauty_title'),
            title=json_data.get('title'),
            user=user,
            coords=coords.save(),
            level=level.save(),
            #images=[Image.objects.create(title=raw_image['title'], image=raw_image['data']) for raw_image in json_data['images']], # я бы так сделал, но джанго решил меня подставить
        )

        if pereval:
            pereval.images.set([image.save() for image in images],)
            pereval.save()

        response_data = {
            'id':pereval.pk
        }
        #return HttpResponse(PerevalSerializer(pereval).data)
        return HttpResponse(json.dumps(response_data), content_type="application/json", status=status.HTTP_201_CREATED, )
