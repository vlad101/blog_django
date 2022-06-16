# Generated by Django 4.0.5 on 2022-06-09 15:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0005_auto_20220424_2025'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', help_text='Enter a title of the post', max_length=250)),
                ('slug', models.SlugField(default='', editable=False, help_text='Slug will be automatically geneted based on the title', max_length=250, unique=True)),
                ('body', models.TextField(help_text='Enter a body of the post', max_length=1000)),
                ('created', models.DateTimeField(default=django.utils.timezone.now, help_text='Select a date to create a post')),
                ('publish', models.DateTimeField(default=django.utils.timezone.now, help_text='Select a date to publish a post')),
                ('updated', models.DateTimeField(default=django.utils.timezone.now, help_text='Select a date to update a post')),
                ('status', models.CharField(blank=True, choices=[('d', 'Draft'), ('p', 'Published')], default='d', help_text='Post status', max_length=1)),
                ('valid', models.BooleanField(default=True, help_text='Set validity of the post')),
                ('author', models.ForeignKey(blank=True, help_text='Select a user for the post', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('tags', taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
            ],
            options={
                'ordering': ['created', 'author'],
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', help_text='Enter a name of the comment', max_length=80)),
                ('body', models.TextField(help_text='Enter a body of the comment', max_length=1000)),
                ('created', models.DateTimeField(default=django.utils.timezone.now, help_text='Select a date to create a comment')),
                ('updated', models.DateTimeField(default=django.utils.timezone.now, help_text='Select a date to update a comment')),
                ('valid', models.BooleanField(default=True, help_text='Set validity of the comment')),
                ('author', models.ForeignKey(blank=True, help_text='Select a user for the comment', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('post', models.ForeignKey(help_text='Select a post for the comment', null=True, on_delete=django.db.models.deletion.SET_NULL, to='blog.post')),
            ],
            options={
                'ordering': ['created'],
            },
        ),
    ]
