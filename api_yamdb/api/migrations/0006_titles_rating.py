# Generated by Django 2.2.6 on 2021-07-16 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_remove_titles_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='titles',
            name='rating',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]