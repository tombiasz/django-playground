from django.conf.urls import url, include

from rest_framework import routers

from . import views_api


router = routers.DefaultRouter()
router.register(r'genre', views_api.GenreViewSet)
router.register(r'language', views_api.LanguageViewSet)

urlpatterns = [
    url(r'^', include(router.urls))
]
