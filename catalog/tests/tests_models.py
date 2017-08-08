from django.test import TestCase

from catalog.models import Author, Genre, Language, Book


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
        self.book.genre.add(genre_1)
        self.book.genre.add(genre_2)
        self.book.genre.add(genre_3)
        self.book.genre.add(genre_4)
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
