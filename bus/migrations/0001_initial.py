# Generated by Django 3.0.4 on 2020-03-10 18:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('next', models.IntegerField()),
                ('prev', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Route',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('distance', models.IntegerField(default=0)),
                ('time', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Stop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('distance', models.IntegerField(default=0)),
                ('time', models.IntegerField(default=0)),
                ('next', models.IntegerField()),
                ('prev', models.IntegerField()),
                ('route', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bus.Route')),
            ],
        ),
        migrations.CreateModel(
            name='BusStopReal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('arrival', models.TimeField()),
                ('departure', models.TimeField()),
                ('bus', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bus.Bus')),
                ('stop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bus.Stop')),
            ],
        ),
        migrations.CreateModel(
            name='BusStop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('arrival', models.TimeField()),
                ('departure', models.TimeField()),
                ('bus', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bus.Bus')),
                ('stop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bus.Stop')),
            ],
        ),
        migrations.AddField(
            model_name='bus',
            name='route',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bus.Route'),
        ),
    ]