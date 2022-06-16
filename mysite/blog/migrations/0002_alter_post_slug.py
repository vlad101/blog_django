# Generated by Django 4.0.5 on 2022-06-09 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='slug',
            field=models.SlugField(default='', help_text='Slug will be automatically generated based on the title', max_length=250, unique=True),
        ),
    ]
