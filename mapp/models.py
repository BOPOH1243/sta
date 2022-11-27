from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.
class User(models.Model):
    email = models.EmailField()
    phone = PhoneNumberField(unique=True, null=False, blank=False)
    name = models.CharField(max_length=64, default='default_name')
    family_name = models.CharField(max_length=64, default='default_fam')
    patronymic = models.CharField(max_length=64, default='default_otc')


class Image(models.Model):
    title = models.CharField(max_length=64, default='default_title')
    image = models.ImageField(upload_to='uploads/%Y/%m/%d/')


class Coords(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    height = models.IntegerField()


class Area(models.Model):
    title = models.CharField(max_length=64, default='default_area')




class Pereval(models.Model):
    STATUSES = [
        'new',
        'pending',
        'accepted',
        'rejected',
    ]
    beauty_title = models.CharField(max_length=64, default='default_beauty_title')
    title = models.CharField(max_length=64, default='default_title')
    other_titles = models.CharField(max_length=64, default='default')
    add_time = models.DateTimeField(auto_now_add=True, editable=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    status = models.CharField(max_length=16, choices=STATUSES, default='new')
    images = models.ManyToManyField(Image, through='PerevalImage')
    coords = models.ForeignKey(Coords, on_delete=models.CASCADE)
    areas = models.ManyToManyField(Area, through='PerevalArea')


class PerevalArea(models.Model):
    area = models.ForeignKey(Area, on_delete=models.CASCADE)
    pereval = models.ForeignKey(Pereval, on_delete=models.CASCADE)



class PerevalImage(models.Model):
    pereval = models.ForeignKey(Pereval, on_delete=models.CASCADE)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)


class Level(models.Model):
    LEVELS = [
        '1А',
        '1Б',
        '2А',
        '2Б',
        '3А',
        '3Б',
    ]
    winter = models.CharField(max_length=2, choices=LEVELS, default=LEVELS[0], )
    summer = models.CharField(max_length=2, choices=LEVELS, default=LEVELS[0], )
    autumn = models.CharField(max_length=2, choices=LEVELS, default=LEVELS[0], )
    spring = models.CharField(max_length=2, choices=LEVELS, default=LEVELS[0], )



