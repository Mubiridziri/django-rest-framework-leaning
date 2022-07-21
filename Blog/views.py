from rest_framework import generics
from Blog.serializers import PostDetailSerializer, PostListSerializer
from Blog.models import Post
from Blog.permissions import IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticated


class PostCreateView(generics.CreateAPIView):
    serializer_class = PostDetailSerializer,
    permission_classes = (IsAuthenticated,)


class PostListView(generics.ListAPIView):
    serializer_class = PostListSerializer
    queryset = Post.objects.all()
    permission_classes = (IsAuthenticated, )


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PostDetailSerializer
    queryset = Post.objects.all()
    permission_classes = (IsOwnerOrReadOnly, )