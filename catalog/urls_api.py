from django.conf.urls import url, include

from rest_framework import routers

from . import views_api


router = routers.DefaultRouter()
router.register(r'genres', views_api.GenreViewSet, 'api-genres')
router.register(r'languages', views_api.LanguageViewSet, 'api-languages')
router.register(r'books', views_api.BookViewSet, 'api-books')
router.register(r'authors', views_api.AuthorViewSet, 'api-authors')

urlpatterns = [
    url(r'^', include(router.urls))
]
