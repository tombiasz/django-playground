from django.test import TestCase

from catalog.models import Author, Book
from django.core.urlresolvers import reverse


class AuthorListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        number_of_authors = 13
        for author_num in range(number_of_authors):
            Author.objects.create(
                first_name='Christian {}'.format(author_num),
                last_name = 'Surname {}'.format(author_num)
            )

    def test_view_url_returns_http_ok(self):
        resp = self.client.get('/catalog/authors/')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_is_accessible_by_url_name(self):
        resp = self.client.get(reverse('author-list'))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('author-list'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'catalog/author_list.html')

    def test_pagination_is_ten(self):
        resp = self.client.get(reverse('author-list'))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] == True)
        self.assertTrue(len(resp.context['author_list']) == 10)


class AuthorDetailsViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = Author.objects.create(
            first_name='Firstname',
            last_name = 'Surname'
        )

    def test_view_url_returns_http_ok(self):
        url = '/catalog/authors/{}'.format(self.author.pk)
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_view_url_is_accessible_by_url_name(self):
        url = reverse('author-detail', kwargs={ 'pk': self.author.pk})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        url = reverse('author-detail', kwargs={ 'pk': self.author.pk})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'catalog/author_detail.html')

    def test_view_passes_author_in_context(self):
        url = reverse('author-detail', kwargs={ 'pk': self.author.pk})
        resp = self.client.get(url)
        self.assertTrue('author' in resp.context)
        self.assertEqual(resp.context['author'], self.author)


class BookListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        number_of_books = 13
        for book_num in range(number_of_books):
            Book.objects.create(
                title='Title {}'.format(book_num),
            )

    def test_view_url_returns_http_ok(self):
        resp = self.client.get('/catalog/books/')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_is_accessible_by_url_name(self):
        resp = self.client.get(reverse('book-list'))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('book-list'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'catalog/book_list.html')

    def test_pagination_is_ten(self):
        resp = self.client.get(reverse('book-list'))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] == True)
        self.assertTrue(len(resp.context['book_list']) == 10)