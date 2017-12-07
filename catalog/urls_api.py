from django.conf.urls import url, include

from rest_framework import routers

from . import views_api


router = routers.DefaultRouter()
router.register(r'genre', views_api.GenreViewSet)

urlpatterns = [
    url(r'^', include(router.urls))
]
