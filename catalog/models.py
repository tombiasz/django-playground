import uuid
from datetime import date

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Genre(models.Model):

    name = models.CharField(max_length=200, help_text="Enter a book genre (e.g. Science Fiction, French Poetry etc.)")

    def __str__(self):
        return self.name


class Language(models.Model):

    name = models.CharField(max_length=100, help_text='Book\'s language')

    def __str__(self):
        return self.name


class Book(models.Model):

    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    summary = models.TextField(max_length=1000, help_text='Enter a brief description of the book')
    isbn = models.CharField('ISBN', max_length=13, help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    genre = models.ManyToManyField(Genre, help_text='Select a genre for this book')
    language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])

    def display_genre(self):
        """
        Return Genre as string. Required for admin list display.
        """
        limit = 3
        return ', '.join((genre.name for genre in self.genre.all()[:limit]))
    display_genre.short_description = 'Genre'


class BookInstance(models.Model):

    MAINTENANCE_STATUS = 'd'
    ON_LOAN_STATUS = 'o'
    AVAILABLE_STATUS = 'a'
    RESERVED_STATUS = 'r'
    LOAN_STATUS = (
        (MAINTENANCE_STATUS, 'Maintenance'),
        (ON_LOAN_STATUS, 'On loan'),
        (AVAILABLE_STATUS, 'Available'),
        (RESERVED_STATUS, 'Reserved'),
    )


    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular book across whole library')
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default=MAINTENANCE_STATUS, help_text='Book availability')
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['due_back']
        permissions = (('can_mark_returned', 'Set book as returned'),)

    def __str__(self):
        if self.book:
            return '{} ({})'.format(self.id, self.book.title)
        return '{}'.format(self.id)

    @property
    def is_overdue(self):
        return self.due_back and date.today() > self.due_back


class Author(models.Model):

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField(null=True, blank=True)

    def __str__(self):
        return '%s, %s' % (self.last_name, self.first_name)

    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])
