from django.test import TestCase

from catalog.models import Author, Genre, Language


class AuthorModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Author.objects.create(first_name="Big", last_name="Bob")

    def test_first_name_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('first_name').verbose_name
        self.assertEqual(field_label, 'first name')

    def test_last_name_labeL(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('last_name').verbose_name
        self.assertEqual(field_label, 'last name')

    def test_date_of_birth_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('date_of_birth').verbose_name
        self.assertEqual(field_label, 'date of birth')

    def test_date_of_death_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('date_of_death').verbose_name
        self.assertEqual(field_label, 'date of death')

    def test_first_name_max_length(self):
        author = Author.objects.get(id=1)
        max_length = author._meta.get_field('first_name').max_length
        self.assertEqual(max_length, 100)

    def test_last_name_max_length(self):
        author = Author.objects.get(id=1)
        max_length = author._meta.get_field('last_name').max_length
        self.assertEqual(max_length, 100)

    def test_object_name_is_first_name_comma_last_name(self):
        author = Author.objects.get(id=1)
        obj_name = '{}, {}'.format(author.last_name, author.first_name)
        self.assertEqual(obj_name, str(author))

    def test_get_absolute_url(self):
        author = Author.objects.get(id=1)
        self.assertEqual(author.get_absolute_url(), '/catalog/authors/1')


class GenreModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Genre.objects.create(name="Poetry")

    def test_name_label(self):
        genre = Genre.objects.get(id=1)
        field_label = genre._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_name_field_hekp_text(self):
        genre = Genre.objects.get(id=1)
        field_label = genre._meta.get_field('name').help_text
        self.assertEqual(field_label, "Enter a book genre (e.g. Science Fiction, French Poetry etc.)")

    def test_name_max_length(self):
        genre = Genre.objects.get(id=1)
        max_length = genre._meta.get_field('name').max_length
        self.assertEqual(max_length, 200)

    def test_object_name_is_name(self):
        genre = Genre.objects.get(id=1)
        obj_name = '{}'.format(genre.name)
        self.assertEqual(obj_name, genre.name)


class LanguageModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Language.objects.create(name="en")

    def test_name_label(self):
        lang = Language.objects.get(id=1)
        field_label = lang._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_name_field_hekp_text(self):
        lang = Language.objects.get(id=1)
        field_label = lang._meta.get_field('name').help_text
        self.assertEqual(field_label, "Book's language")

    def test_name_max_length(self):
        lang = Language.objects.get(id=1)
        max_length = lang._meta.get_field('name').max_length
        self.assertEqual(max_length, 100)

    def test_object_name_is_name(self):
        lang = Language.objects.get(id=1)
        obj_name = '{}'.format(lang.name)
        self.assertEqual(obj_name, lang.name)