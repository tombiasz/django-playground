from django.contrib import admin

from .models import Author, Book, BookInstance, Genre


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    pass


admin.site.register(BookInstance)
admin.site.register(Genre)
