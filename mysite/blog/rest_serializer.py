from rest_framework import permissions
from rest_framework.serializers import ModelSerializer
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveAPIView
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope

from .models import Post

class PostSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

# Create the Post API views
class PostList(ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class PostDetails(RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    queryset = Post.objects.all()
    serializer_class = PostSerializer