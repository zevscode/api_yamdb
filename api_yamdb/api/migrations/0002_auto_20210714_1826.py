# Generated by Django 2.2.6 on 2021-07-14 15:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Имя категории')),
                ('slug', models.SlugField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Genres',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Нзавание жанра')),
                ('slug', models.SlugField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='GenresTitles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genres', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.Genres')),
            ],
        ),
        migrations.CreateModel(
            name='Titles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=258, verbose_name='Название')),
                ('year', models.IntegerField(default=0, verbose_name='Год выпуска')),
                ('description', models.TextField(max_length=258, verbose_name='Описание')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.Category', verbose_name='Категории')),
                ('genre', models.ManyToManyField(through='api.GenresTitles', to='api.Genres')),
            ],
        ),
        migrations.AddField(
            model_name='genrestitles',
            name='titles',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.Titles'),
        ),
    ]
