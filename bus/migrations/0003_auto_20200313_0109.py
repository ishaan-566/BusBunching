# Generated by Django 3.0.4 on 2020-03-12 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bus', '0002_auto_20200313_0102'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bus',
            name='next',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='bus',
            name='prev',
            field=models.CharField(max_length=30),
        ),
    ]