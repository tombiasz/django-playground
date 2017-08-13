import datetime
import uuid

from django.test import TestCase
from django.contrib.auth.models import User

from catalog.models import Author, Genre, Language, Book, BookInstance


class AuthorModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = Author.objects.create(first_name="Big", last_name="Bob")

    def setUp(self):
        self.author.refresh_from_db()

    def test_first_name_label(self):
        field_label = self.author._meta.get_field('first_name').verbose_name
        self.assertEqual(field_label, 'first name')

    def test_last_name_labeL(self):
        field_label = self.author._meta.get_field('last_name').verbose_name
        self.assertEqual(field_label, 'last name')

    def test_date_of_birth_label(self):
        field_label = self.author._meta.get_field('date_of_birth').verbose_name
        self.assertEqual(field_label, 'date of birth')

    def test_date_of_death_label(self):
        field_label = self.author._meta.get_field('date_of_death').verbose_name
        self.assertEqual(field_label, 'date of death')

    def test_first_name_max_length(self):
        max_length = self.author._meta.get_field('first_name').max_length
        self.assertEqual(max_length, 100)

    def test_last_name_max_length(self):
        max_length = self.author._meta.get_field('last_name').max_length
        self.assertEqual(max_length, 100)

    def test_object_name_is_first_name_comma_last_name(self):
        obj_name = '{}, {}'.format(self.author.last_name, self.author.first_name)
        self.assertEqual(obj_name, str(self.author))

    def test_get_absolute_url(self):
        self.assertEqual(self.author.get_absolute_url(), '/catalog/authors/1')


class GenreModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.genre = Genre.objects.create(name="Poetry")

    def setUp(self):
        self.genre.refresh_from_db()

    def test_name_label(self):
        field_label = self.genre._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_name_field_hekp_text(self):
        field_label = self.genre._meta.get_field('name').help_text
        self.assertEqual(field_label, "Enter a book genre (e.g. Science Fiction, French Poetry etc.)")

    def test_name_max_length(self):
        max_length = self.genre._meta.get_field('name').max_length
        self.assertEqual(max_length, 200)

    def test_object_name_is_name(self):
        obj_name = '{}'.format(self.genre.name)
        self.assertEqual(obj_name, self.genre.name)


class LanguageModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.lang = Language.objects.create(name="en")

    def setUp(self):
        self.lang.refresh_from_db()

    def test_name_label(self):
        field_label = self.lang._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_name_field_help_text(self):
        field_label = self.lang._meta.get_field('name').help_text
        self.assertEqual(field_label, "Book's language")

    def test_name_max_length(self):
        max_length = self.lang._meta.get_field('name').max_length
        self.assertEqual(max_length, 100)

    def test_object_name_is_name(self):
        obj_name = '{}'.format(self.lang.name)
        self.assertEqual(obj_name, self.lang.name)


class BookModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.book = Book.objects.create(title="Book title")

    def setUp(self):
        self.book.refresh_from_db()

    def test_title_label(self):
        field_label = self.book._meta.get_field('title').verbose_name
        self.assertEqual(field_label, 'title')

    def test_title_max_length(self):
        max_length = self.book._meta.get_field('title').max_length
        self.assertEqual(max_length, 200)

    def test_author_label(self):
        field_label = self.book._meta.get_field('author').verbose_name
        self.assertEqual(field_label, 'author')

    def test_author_allow_null_value(self):
        self.assertIsNone(self.book.author)

    def test_author_set_null_on_delte(self):
        author = Author.objects.create(first_name="Bob", last_name="Smith")
        self.book.author = author
        self.book.save()
        self.book.refresh_from_db()
        self.assertEqual(self.book.author, author)
        author.delete()
        self.book.refresh_from_db()
        self.assertIsNone(self.book.author)

    def test_summary_label(self):
        field_label = self.book._meta.get_field('summary').verbose_name
        self.assertEqual(field_label, 'summary')

    def test_summary_max_length(self):
        max_length = self.book._meta.get_field('summary').max_length
        self.assertEqual(max_length, 1000)

    def test_summary_field_help_text(self):
        field_label = self.book._meta.get_field('summary').help_text
        self.assertEqual(field_label, "Enter a brief description of the book")

    def test_isbn_label(self):
        field_label = self.book._meta.get_field('isbn').verbose_name
        self.assertEqual(field_label, 'ISBN')

    def test_isbn_max_length(self):
        max_length = self.book._meta.get_field('isbn').max_length
        self.assertEqual(max_length, 13)

    def test_isbn_field_help_text(self):
        field_label = self.book._meta.get_field('isbn').help_text
        self.assertEqual(field_label, '13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')

    def test_genre_label(self):
        field_label = self.book._meta.get_field('genre').verbose_name
        self.assertEqual(field_label, 'genre')

    def test_genre_field_help_text(self):
        field_label = self.book._meta.get_field('genre').help_text
        self.assertEqual(field_label, 'Select a genre for this book')

    def test_display_genre_displays_genre_name(self):
        genre = Genre.objects.create(name='1')
        self.book.genre.add(genre)
        self.book.refresh_from_db()
        expected = '{}'.format(genre.name)
        self.assertEqual(self.book.display_genre(), expected)

    def test_display_genre_method_displays_only_3_objects(self):
        genre_1 = Genre.objects.create(name='1')
        genre_2 = Genre.objects.create(name='2')
        genre_3 = Genre.objects.create(name='3')
        genre_4 = Genre.objects.create(name='4')
        self.book.genre.add(genre_1, genre_2, genre_3, genre_4)
        self.book.refresh_from_db()
        self.assertEqual(self.book.genre.count(), 4)
        expected = ', '.join([genre_1.name, genre_2.name, genre_3.name])
        self.assertEqual(self.book.display_genre(), expected)

    def test_language_label(self):
        field_label = self.book._meta.get_field('language').verbose_name
        self.assertEqual(field_label, 'language')

    def test_language_allow_null_value(self):
        self.assertIsNone(self.book.language)

    def test_language_set_null_on_delte(self):
        lang = Language.objects.create(name='en')
        self.book.language = lang
        self.book.save()
        self.book.refresh_from_db()
        self.assertEqual(self.book.language, lang)
        lang.delete()
        self.book.refresh_from_db()
        self.assertIsNone(self.book.language)

    def test_object_name_is_title(self):
        obj_name = '{}'.format(self.book.title)
        self.assertEqual(obj_name, self.book.title)

    def test_get_absolute_url(self):
        self.assertEqual(self.book.get_absolute_url(), '/catalog/books/1')


class BookInstanceModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.book_instance = BookInstance.objects.create(imprint="imprint")

    def setUp(self):
        self.book_instance.refresh_from_db()

    def test_id_label(self):
        field_label = self.book_instance._meta.get_field('id').verbose_name
        self.assertEqual(field_label, 'id')

    def test_id_field_help_text(self):
        field_label = self.book_instance._meta.get_field('id').help_text
        self.assertEqual(field_label, "Unique ID for this particular book across whole library")

    def test_id_field_is_primary_key(self):
        self.assertEqual(self.book_instance.id, self.book_instance.pk)

    def test_id_field_default_is_proper_uuid(self):
        try:
            uuid.UUID(str(self.book_instance.id), version=4)
        except:
            self.fail('id default value is not a proper UUID')

    def test_book_label(self):
        field_label = self.book_instance._meta.get_field('book').verbose_name
        self.assertEqual(field_label, 'book')

    def test_book_allow_null_value(self):
        self.assertIsNone(self.book_instance.book)

    def test_book_is_set_to_null_on_book_delte(self):
        book = Book.objects.create(title="Book title")
        self.book_instance.book = book
        self.book_instance.save()
        self.book_instance.refresh_from_db()
        self.assertEqual(self.book_instance.book, book)
        book.delete()
        self.book_instance.refresh_from_db()
        self.assertIsNone(self.book_instance.book)

    def test_imprint_label(self):
        field_label = self.book_instance._meta.get_field('imprint').verbose_name
        self.assertEqual(field_label, 'imprint')

    def test_imprint_max_length(self):
        max_length = self.book_instance._meta.get_field('imprint').max_length
        self.assertEqual(max_length, 200)

    def test_due_back_label(self):
        field_label = self.book_instance._meta.get_field('due_back').verbose_name
        self.assertEqual(field_label, 'due back')

    def test_due_back_allow_null_value(self):
        self.assertIsNone(self.book_instance.due_back)

    def test_due_back_can_be_blank(self):
        can_be_blank = self.book_instance._meta.get_field('due_back').blank
        self.assertTrue(can_be_blank)

    def test_status_label(self):
        field_label = self.book_instance._meta.get_field('status').verbose_name
        self.assertEqual(field_label, 'status')

    def test_status_max_length(self):
        max_length = self.book_instance._meta.get_field('status').max_length
        self.assertEqual(max_length, 1)

    def test_status_field_help_text(self):
        field_label = self.book_instance._meta.get_field('status').help_text
        self.assertEqual(field_label, "Book availability")

    def test_status_can_be_blank(self):
        can_be_blank = self.book_instance._meta.get_field('status').blank
        self.assertTrue(can_be_blank)

    def test_status_field_default_is_to_maintaince(self):
        self.assertEqual(self.book_instance.status, 'd')

    def test_status_field_choices_is_set_to_loan_statuses(self):
        choices = self.book_instance._meta.get_field('status').choices
        self.assertEqual(choices, BookInstance.LOAN_STATUS)

    def test_borrower_label(self):
        field_label = self.book_instance._meta.get_field('borrower').verbose_name
        self.assertEqual(field_label, 'borrower')

    def test_borrower_can_be_blank(self):
        can_be_blank = self.book_instance._meta.get_field('borrower').blank
        self.assertTrue(can_be_blank)

    def test_borrower_allow_null_value(self):
        self.assertIsNone(self.book_instance.borrower)

    def test_borrower_is_set_to_null_on_user_delte(self):
        user = User.objects.create(username="test", password="test")
        self.book_instance.borrower = user
        self.book_instance.save()
        self.book_instance.refresh_from_db()
        self.assertEqual(self.book_instance.borrower, user)
        user.delete()
        self.book_instance.refresh_from_db()
        self.assertIsNone(self.book_instance.borrower)

    def test_object_name_is_id_and_title(self):
        book = Book.objects.create(title="Book title")
        self.book_instance.book = book
        self.book_instance.save()
        obj_name = '{} ({})'.format(self.book_instance.id, self.book_instance.book.title)
        self.assertEqual(obj_name, str(self.book_instance))

    def test_objects_are_ordered_by_due_date(self):
        self.assertEqual(BookInstance._meta.ordering, ['due_back'])

    def test_model_permissions(self):
        expected = (('can_mark_returned', 'Set book as returned'),)
        self.assertEqual(BookInstance._meta.permissions, expected)

    def test_is_overdue_if_due_back_is_not_set(self):
        self.assertFalse(self.book_instance.is_overdue)

    def test_is_overdue_if_due_back_is_tomorrow(self):
        today = datetime.date.today()
        tomorrow = today + datetime.timedelta(days=1)
        self.book_instance.due_back = tomorrow
        self.book_instance.save()
        self.assertFalse(self.book_instance.is_overdue)

    def test_is_overdue_if_due_back_was_yesterday(self):
        today = datetime.date.today()
        yesterday = today + datetime.timedelta(days=-1)
        self.book_instance.due_back = yesterday
        self.book_instance.save()
        self.assertTrue(self.book_instance.is_overdue)

    def test_is_overdue_if_due_back_is_today(self):
        today = datetime.date.today()
        self.book_instance.due_back = today
        self.book_instance.save()
        self.assertFalse(self.book_instance.is_overdue)
