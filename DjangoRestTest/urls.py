from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/drf-auth/', include('rest_framework.urls')),
    path('api/v1/blog/', include('Blog.urls'), name="Blog API"),
    path('api/v1/auth/', include('djoser.urls'), name="Auth with Djoser"),
    path('api/v1/auth_token/', include('djoser.urls.authtoken'), name="Token Auth with Djoser"),
]
