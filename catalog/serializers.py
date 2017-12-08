from rest_framework import serializers

from .models import Genre, Language


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name',)


class LanguageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Language
        fields = ('name',)