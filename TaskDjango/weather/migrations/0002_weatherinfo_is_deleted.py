# Generated by Django 4.2.1 on 2023-05-07 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='weatherinfo',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
    ]
