from django.urls import path
from Blog.views import *


app_name = 'blog'
urlpatterns = [
    path('posts/create/', PostCreateView.as_view(), name="Creating Post"),
    path('posts/all/', PostListView.as_view(), name="Posts List"),
    path('posts/detail/<int:pk>', PostDetailView.as_view(), name="View, Update and Delete"),
]