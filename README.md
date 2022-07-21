# Learning Django with DRF (Django Rest Framework)

## Creating project

```bash
django-admin startproject <project_name>
```

## Create virtual environment 
(need package python3-virtualenv)

```bash
virtualenv <project_name>
```

## Activate Virtual Environment

```bash
source <project_name>/local/bin/activate
```

* If you need add your virtual env to PyCharm open Settings -> Project <name> -> Python Interpreter -> Show All -> Use exists virtual env -> Select path to <name>/local/bin/python

## Install Django to Virtual Env

```bash
pip install Django
```

## Run migrations for database preparing

```bash
./manage.py migrate
```

## Project Configuring

Open `<project_name>/<project_name>/settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```
You can change database type and learn additional parameters on [this resource](https://docs.djangoproject.com/en/4.0/ref/settings/#databases).

For example PGSQL Config:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'mydatabase',
        'USER': 'mydatabaseuser',
        'PASSWORD': 'mypassword',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}
```

## Start Built-In Server

```bash
./manage.py runserver
```

If you need share project to local network you need add `0.0.0.0` to `ALLOWED_HOSTS` array in `settings.py` and
use another command:
```bash
./manage.py runserver 0.0.0.0:8000
```

You can access to project with `localhost:8000` address and `<your local ip>:8000` for your local network.

## Installing Django Rest Framework (DRF)

```bash
pip install djangorestframework
```

Next, you need add `rest_framework` application to `INSTALLED_APPS` in `settings.py` 

## Creating App in your Project

```bash
./manage.py startapp <app_name>
```

Next, need to create few empty files for future.

```bash
touch <app_name>/urls.py
touch <app_name>/serializers.py
```

## Connect your App to Project

Open `settings.py` and add `<app_name>` to `INSTALLED_APPS`

For example:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'Blog' # <- this my <app_name>
]
```

Including your app urls to project urls, for it you need open `<project_name>/urls.py`
 * Add import `include` in `from django.urls import path` (result: `from django.urls import path, include`)
 * Include path in urlpatterns (`path('', include('<app_name>.urls'))`)

Result file:

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/blog/', include('Blog.urls'))
]
```

## Creating models in `<app_name>/models.py`

```python
from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()


class Post(models.Model):
    title = models.CharField(verbose_name="Title", max_length=150)
    content = models.CharField(verbose_name="Content", max_length=1000)
    pub_date = models.DateTimeField(verbose_name="Published At", auto_now=True)
    POST_STATES = (
        (1, 'Draft '),
        (2, 'Published'),
        (3, 'Archived')
    )
    state = models.IntegerField(verbose_name="State", choices=POST_STATES)
    author = models.ForeignKey(User, verbose_name="Author", on_delete=models.CASCADE)

```

**WARNING**: Always need import user model with help `get_user_model`, because user model can be overridden.
```python
from django.contrib.auth import get_user_model
User = get_user_model()
```

## Creating Views

Write code in `views.py`
```python
from rest_framework import generics
from Blog.serializers import PostDetailSerializer


class PostCreateView(generics.CreateAPIView):
    serializer_class = PostDetailSerializer

```

But for work this code need to create a serializer `PostDetailSerializer` in
`serializers.py`
```python
from rest_framework import serializers
from Blog.models import Post


class PostDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
```

## Creating superuser with help CLI

```bash
./manage.py createsuperuser
```

## Preparing urls in your App
`<app_name>/urls.py`
```python
from django.urls import path
from Blog.views import *

app_name = 'blog'
urlpatterns = [
    path('posts/create/', PostCreateView.as_view())
]
```

## Make migrations

```bash
./manage.py makemigrations
./manage.py migrate
```

## Open UI Tool for working with basic API

Start server

```bash
./manage.py runserver
```

Open link in browser:

`
http://127.0.0.1:8000/api/v1/blog/posts/create/
`

## Manual fixing database migration conflict with help Python Shell

Open shell:

```bash
./manage.py shell
```

Write code :)

## Creating List API

1. Creating Serializer
```python
class PostListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title', 'author', 'state')
```

2. Creating View
```python
class PostListView(generics.ListAPIView):
    serializer_class = PostListSerializer
    queryset = Post.objects.all()
```

3. Creating URL
```python
path('posts/list', PostListView.as_view(), name="Posts List"),
```

## Creating View, Update, Delete API

1. Creating View

```python
class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PostDetailSerializer
    queryset = Post.objects.all()
```

2. Creating URL

```python
path('posts/detail/<int:pk>', PostDetailView.as_view(), name="View, Update and Delete"),
```

Allow: GET, PUT, PATCH, DELETE, HEAD, OPTIONS


## Hidden Fields

Update exist PostDetailSerializer like this:

```python
class PostDetailSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault()) # <-- New Line
    
    class Meta:
        model = Post
        fields = '__all__'
```

## Implement Basic Rest Authorization from Django

Add code like this to <project_name>/urls.py

```python
path('api/v1/drf-auth/', include('rest_framework.urls')),
```

## Permissions

Create file `<app_name>/permissions.py` and write base permission:

```python
from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user

```

And update your view:

```python
from rest_framework import generics
from Blog.serializers import PostDetailSerializer, PostListSerializer
from Blog.models import Post
from Blog.permissions import IsOwnerOrReadOnly # <--- new import


class PostCreateView(generics.CreateAPIView):
    serializer_class = PostDetailSerializer


class PostListView(generics.ListAPIView):
    serializer_class = PostListSerializer
    queryset = Post.objects.all()


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PostDetailSerializer
    queryset = Post.objects.all()
    permission_classes = (IsOwnerOrReadOnly, ) # <-- connect your permission
```

## View Only Full Authenticated

```python
from rest_framework import generics
from Blog.serializers import PostDetailSerializer, PostListSerializer
from Blog.models import Post
from Blog.permissions import IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticated # <-- Import django permission


class PostCreateView(generics.CreateAPIView):
    serializer_class = PostDetailSerializer,
    permission_classes = (IsAuthenticated,) # <-- connect this permission to view


class PostListView(generics.ListAPIView):
    serializer_class = PostListSerializer
    queryset = Post.objects.all()
    permission_classes = (IsAuthenticated, )


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PostDetailSerializer
    queryset = Post.objects.all()
    permission_classes = (IsOwnerOrReadOnly, )
```


