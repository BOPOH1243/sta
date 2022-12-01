from rest_framework import routers
from .views import *
from django.urls import path, include


router = routers.DefaultRouter()
router.register(r'levels', LevelViewset)
router.register(r'perevals', PerevalViewset)
router.register(r'users', UserViewset)
router.register(r'coords', CoordsViewset)
router.register(r'images', ImageViewset)
router.register(r'areas', AreaViewset)


urlpatterns = [
    path('', include(router.urls)),
    path('submitdata/', submitData)
]