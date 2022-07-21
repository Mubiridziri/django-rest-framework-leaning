from rest_framework import generics
from Blog.serializers import PostDetailSerializer, PostListSerializer
from Blog.models import Post


class PostCreateView(generics.CreateAPIView):
    serializer_class = PostDetailSerializer


class PostListView(generics.ListAPIView):
    serializer_class = PostListSerializer
    queryset = Post.objects.all()


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PostDetailSerializer
    queryset = Post.objects.all()