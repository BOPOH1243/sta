# Generated by Django 4.1.3 on 2022-11-29 00:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mapp', '0002_alter_level_autumn_alter_level_spring_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='pereval',
            name='level',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='mapp.level'),
            preserve_default=False,
        ),
    ]
