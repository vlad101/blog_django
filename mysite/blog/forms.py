from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from django.forms import ModelForm


from .models import Comment, Post

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['id', 'name', 'body', 'author', 'post', 'updated']
        widgets = {
                    'id': forms.HiddenInput(),
                    'author': forms.HiddenInput(),
                    'post': forms.HiddenInput(),
                    'updated': forms.HiddenInput(),
                }

class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['author', 'title', 'slug', 'body', 'updated', 'publish', 'tags', 'status']
        widgets = {
                    'author': forms.HiddenInput(),
                    'updated': forms.HiddenInput(),
                    'publish': forms.HiddenInput(),
                    'slug': forms.HiddenInput(),
        }