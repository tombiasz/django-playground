from rest_framework import serializers

from .models import Genre, Language, Book, Author, BookInstance


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


class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Author
        # fields = ('first_name', 'last_name', 'date_of_birth', 'date_of_death')
        fields = '__all__'


class BookInstanceSerializer(serializers.ModelSerializer):

    class Meta:
        model = BookInstance
        fields = '__all__'