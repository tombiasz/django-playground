from django.test import TestCase

from catalog.models import Author, Genre, Language


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