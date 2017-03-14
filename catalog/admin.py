from django.contrib import admin

from .models import Author, Book, BookInstance, Genre


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    pass

admin.site.register(Book)
admin.site.register(BookInstance)
admin.site.register(Genre)
