from django.contrib import admin
from django.urls import path, re_path, include
from django.views.static import serve

from cash_register import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('register_app.urls')),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]
