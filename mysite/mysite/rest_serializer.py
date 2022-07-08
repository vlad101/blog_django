from django.contrib.auth.models import User, Group
from rest_framework import permissions
from rest_framework.serializers import ModelSerializer
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveAPIView
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope

from blog.models import Post


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', "first_name", "last_name")

class GroupSerializer(ModelSerializer):
    class Meta:
        model = Group
        fields = ("name", )

class PostSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

# Create the User API views
class UserList(ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetails(RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    queryset = User.objects.all()
    serializer_class = UserSerializer

# Create the Group API views
class GroupList(ListAPIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasScope]
    required_scopes = ['groups']
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

# Create the Post API views
class PostList(ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class PostDetails(RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    queryset = Post.objects.all()
    serializer_class = PostSerializer