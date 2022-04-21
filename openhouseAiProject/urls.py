from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from log_manager import views

router = DefaultRouter()
router.register('logs', views.LogViewSet, basename="api")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls))
]
