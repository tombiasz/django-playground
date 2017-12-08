from rest_framework import serializers

from .models import Genre, Language, Book


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name',)


class LanguageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Language
        fields = ('name',)


class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = ('title', 'author', 'summary', 'isbn', 'genre', 'language' )