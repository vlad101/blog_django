from datetime import date
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.timezone import now
from taggit.managers import TaggableManager

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, help_text="Select a user for the post")
    title = models.CharField(max_length=250, null=False, default='', help_text="Enter a title of the post")
    slug = models.SlugField(max_length=250, null=False, default='', unique=True, help_text="Slug will be automatically generated based on the title")
    body = models.TextField(max_length=1000, help_text="Enter a body of the post")
    created = models.DateTimeField(default=now, null=False, help_text="Select a date to create a post")
    publish = models.DateTimeField(default=now, null=False, help_text="Select a date to publish a post")
    updated = models.DateTimeField(default=now, null=False, help_text="Select a date to update a post")
    status = models.CharField(
        max_length=1,
        choices=(
            ('d', 'Draft'),
            ('p', 'Published'),
        ),
        blank=True,
        default='d',
        help_text='Post status'
    )
    valid = models.BooleanField(default=True, help_text="Set validity of the post")
    tags = TaggableManager()

    class Meta:
        ordering = ['created', 'author']

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={
                                        'year': self.created.year,
                                        'month': self.created.month,
                                        'day': self.created.day,
                                        'slug': self.slug,
                                    }
                        )

    def __str__(self):
        return self.title

class Comment(models.Model):
    name = models.CharField(max_length=80, null=False, default='', help_text="Enter a name of the comment")
    body = models.TextField(max_length=1000, help_text="Enter a body of the comment")
    created = models.DateTimeField(default=now, null=False, help_text="Select a date to create a comment")
    updated = models.DateTimeField(default=now, null=False, help_text="Select a date to update a comment")
    valid = models.BooleanField(default=True, null=False, help_text="Set validity of the comment")
    post = models.ForeignKey('Post', on_delete=models.SET_NULL, null=True, help_text="Select a post for the comment")
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, help_text="Select a user for the comment")

    class Meta:
        ordering = ['created']

    def __str__(self):
        return self.name