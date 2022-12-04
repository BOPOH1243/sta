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
def submitData(request):
    if request.method == 'POST':
        json_params = json.loads(request.body)
        json_data = json_params
        images = [
            ImageFuckedSerializer(
                data={
                    'title': raw_image.get('title'),
                    'imagehex': raw_image.get('data'),
                }

            )
            for raw_image in json_data.get('images')
        ]
        for image in images:
            if image.is_valid()==False:
                return HttpResponse(json.dumps({'message':'image is not valid'}), content_type="application/json", status=status.HTTP_400_BAD_REQUEST,)
        pereval = SubmitDataSerializer(
            data={
                "beauty_title": json_data.get('beauty_title'),
                "title": json_data.get('title'),
                "other_titles": json_data.get('other_titles'),
                'level': LevelSerializer(data=json_data.get('level', {})),
                'user': UserSerializer(data={
                    'email': json_data.get('user', {}).get('email'),
                    'phone': json_data.get('user', {}).get('phone'),
                    'name': json_data.get('user', {}).get('name'),
                    'family_name': json_data.get('user', {}).get('fam'),
                    'patronymic': json_data.get('user', {}).get('otc')
                }),
                'coords': CoordsSerializer(data=json_data.get('coords', {}))
            }
        )
        tsr=SubmitDataSerializer(instance=Pereval.objects.get())
        return HttpResponse(json.dumps(tsr.data), content_type="application/json", status=status.HTTP_400_BAD_REQUEST, )
        print(pereval.is_valid())
        print(pereval.validated_data)
        if pereval.is_valid():
            pereval = pereval.save()
            pereval.images.set([image.save() for image in images], )
            pereval.save()
        else:
            return HttpResponse(json.dumps({'message': 'pereval is not valid'}), content_type="application/json", status=status.HTTP_400_BAD_REQUEST, )



        response_data = {
            'id': pereval.pk
        }
        #return HttpResponse(PerevalSerializer(pereval).data)
        return HttpResponse(json.dumps(response_data), content_type="application/json", status=status.HTTP_201_CREATED, )
