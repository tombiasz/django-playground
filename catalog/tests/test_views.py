import datetime
import uuid

from django.contrib.auth.models import User, Permission
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils import timezone

from catalog.models import Author, Book, BookInstance,Language, Genre


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


class BookDetailsViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.book = Book.objects.create(
            title = 'Title'
        )

    def test_view_url_returns_http_ok(self):
        url = '/catalog/books/{}'.format(self.book.pk)
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_view_url_is_accessible_by_url_name(self):
        url = reverse('book-detail', kwargs={ 'pk': self.book.pk})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        url = reverse('book-detail', kwargs={ 'pk': self.book.pk})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'catalog/book_detail.html')

    def test_view_passes_book_in_context(self):
        url = reverse('book-detail', kwargs={ 'pk': self.book.pk})
        resp = self.client.get(url)
        self.assertTrue('book' in resp.context)
        self.assertEqual(resp.context['book'], self.book)


class LoanedBookInstancesByUserListViewTest(TestCase):

    def setUp(self):
        # create users
        user1 = User.objects.create_user(
            username='testuser1',
            password='12345'
        )
        user2 = User.objects.create_user(
            username='testuser2',
            password='12345'
        )

        # create book
        author = Author.objects.create(first_name = 'John', last_name='Smith')
        genre = Genre.objects.create(name = 'Fantasy')
        language = Language.objects.create(name = 'English')
        book = Book.objects.create(
            title = 'Book Title',
            summary = 'My book summary',
            isbn = 'ABCDEFG',
            author = author,
            language = language,
        )
        book.genre.add(genre)

        # create 30 book instances
        number_of_book_copies = 30
        for book_copy in range(number_of_book_copies):
            return_date = timezone.now() + datetime.timedelta(days = book_copy % 5)
            if book_copy % 2:
                borrower = user1
            else:
                borrower = user2
            status = BookInstance.AVAILABLE_STATUS
            BookInstance.objects.create(
                book=book,
                imprint='Imprint',
                due_back=return_date,
                borrower=borrower,
                status=status
            )

    def _login(self):
        return self.client.login(username='testuser1', password='12345')

    def test_redirect_if_not_logged_in(self):
        resp = self.client.get(reverse('my-borrowed'))
        self.assertRedirects(resp, '/accounts/login/?next=/catalog/mybooks/')

    def test_view_url_returns_http_ok_for_logged_in_user(self):
        self._login()
        resp = self.client.get(reverse('my-borrowed'))
        self.assertEqual(resp.status_code, 200)

        # check our user is logged in
        self.assertEqual(str(resp.context['user']), 'testuser1')

    def test_logged_in_uses_correct_template(self):
        self._login()
        resp = self.client.get(reverse('my-borrowed'))
        self.assertTemplateUsed(resp, 'catalog/bookinstance_list_borrowed_by_user.html')

    def test_view_passes_bookinstance_list_in_context(self):
        self._login()
        resp = self.client.get(reverse('my-borrowed'))
        self.assertTrue('bookinstance_list' in resp.context)

    def test_pagination_is_ten(self):
        self._login()
        resp = self.client.get(reverse('my-borrowed'))

        # change all the book instances to be on loan
        books = BookInstance.objects.filter(borrower=resp.context['user'])
        books.update(status=BookInstance.ON_LOAN_STATUS)

        # refresh page
        resp = self.client.get(reverse('my-borrowed'))

        # check pagination settings
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] == True)
        self.assertTrue(len(resp.context['page_obj']) == 10)

    def test_only_borrowed_books_in_list(self):
        self._login()
        resp = self.client.get(reverse('my-borrowed'))

        # check that initially we don't have any books in list (none on loan)
        self.assertTrue('bookinstance_list' in resp.context)
        self.assertEqual(len(resp.context['bookinstance_list']), 0)

        # now change some book instances to be on loan
        number_of_books = 10
        books = BookInstance.objects.all()[:number_of_books]
        for book_instance in books:
            book_instance.statys = BookInstance.ON_LOAN_STATUS
            book_instance.save()

        # refresh page
        resp = self.client.get(reverse('my-borrowed'))

        # confirm all books belong to our user and are on loan
        for book_instance in resp.context['bookinstance_list']:
            self.assertEqual(resp.context['user'], book_instance.borrower)
            self.assertEqual(book_instance.status, BookInstance.ON_LOAN_STATUS)

    def test_pages_ordered_by_due_date(self):
        self._login()
        resp = self.client.get(reverse('my-borrowed'))

        # change all the book instances to be on loan
        books = BookInstance.objects.filter(borrower=resp.context['user'])
        books.update(status=BookInstance.ON_LOAN_STATUS)

        # refresh page
        resp = self.client.get(reverse('my-borrowed'))

        last_date=0
        for book_instance in resp.context['bookinstance_list']:
            if last_date == 0:
                last_date = book_instance.due_back
            else:
                self.assertTrue(last_date <= book_instance.due_back)



class RenewBookInstancesViewTest(TestCase):

    def setUp(self):
        # create user
        user1 = User.objects.create_user(
            username='testuser1',
            password='12345'
        )

        user2 = User.objects.create_user(
            username='testuser2',
            password='12345'
        )
        permission = Permission.objects.get(name='Set book as returned')
        user2.user_permissions.add(permission)
        user2.save()

        # create book
        author = Author.objects.create(first_name = 'John', last_name='Smith')
        genre = Genre.objects.create(name = 'Fantasy')
        language = Language.objects.create(name = 'English')
        book = Book.objects.create(
            title = 'Book Title',
            summary = 'My book summary',
            isbn = 'ABCDEFG',
            author = author,
            language = language,
        )
        book.genre.add(genre)

        return_date = datetime.date.today() + datetime.timedelta(days=5)

        # create one book instance for each user
        self.bookinstance1 = BookInstance.objects.create(
            book=book,
            imprint='Imprint',
            due_back=return_date,
            borrower=user1,
            status=BookInstance.ON_LOAN_STATUS
        )
        self.bookinstance2 = BookInstance.objects.create(
            book=book,
            imprint='Imprint',
            due_back=return_date,
            borrower=user2,
            status=BookInstance.ON_LOAN_STATUS
        )

    def test_redirect_if_not_logged_in(self):
        resp = self.client.get(reverse(
            'renew-book-librarian',
            kwargs={'pk': self.bookinstance1.pk,}
        ))
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(resp.url.startswith('/accounts/login/') )

    def test_redirect_if_logged_in_but_not_correct_permission(self):
        login = self.client.login(username='testuser1', password='12345')
        resp = self.client.get(reverse(
            'renew-book-librarian',
            kwargs={'pk': self.bookinstance1.pk,}
        ))
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(resp.url.startswith('/accounts/login/') )

    def test_logged_in_with_permission_borrowed_book(self):
        login = self.client.login(username='testuser2', password='12345')
        resp = self.client.get(reverse(
            'renew-book-librarian',
            kwargs={'pk': self.bookinstance2.pk,}
        ))
        self.assertEqual(resp.status_code, 200)

    def test_logged_in_with_permission_another_users_borrowed_book(self):
        login = self.client.login(username='testuser2', password='12345')
        resp = self.client.get(reverse(
            'renew-book-librarian',
            kwargs={'pk': self.bookinstance1.pk,}
        ))
        self.assertEqual(resp.status_code, 200)

    def test_http404_for_invalid_book_if_logged_in(self):
        uid = uuid.uuid4()  # unlikely UID to match our book instance
        login = self.client.login(username='testuser2', password='12345')
        resp = self.client.get(reverse(
            'renew-book-librarian',
            kwargs={'pk': uid}
        ))
        self.assertEqual(resp.status_code, 404)

    def test_view_returns_http_ok_for_logged_in_user_with_permission(self):
        login = self.client.login(username='testuser2', password='12345')
        resp = self.client.get(reverse(
            'renew-book-librarian',
            kwargs={'pk': self.bookinstance1.pk,}
        ))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        login = self.client.login(username='testuser2', password='12345')
        resp = self.client.get(reverse(
            'renew-book-librarian',
            kwargs={'pk': self.bookinstance1.pk,}
        ))
        self.assertTemplateUsed(resp, 'catalog/book_renew_librarian.html')

    def test_redirects_to_all_borrowed_book_list_on_success(self):
        login = self.client.login(username='testuser2', password='12345')
        valid_date = datetime.date.today() + datetime.timedelta(weeks=2)
        url = reverse(
            'renew-book-librarian',
            kwargs={'pk': self.bookinstance1.pk}
        )
        resp = self.client.post(url, {'renewal_date': valid_date})
        self.assertRedirects(resp, reverse('borrowed') )

    def test_form_invalid_renewal_date_past(self):
        login = self.client.login(username='testuser2', password='12345')
        invalid_date_in_past = datetime.date.today() - datetime.timedelta(weeks=1)
        url = reverse(
            'renew-book-librarian',
            kwargs={'pk': self.bookinstance1.pk}
        )
        resp = self.client.post(url, {'renewal_date': invalid_date_in_past} )
        self.assertEqual(resp.status_code, 200)
        self.assertFormError(
            resp,
            'form',
            'renewal_date',
            'Invalid date - renewal in past'
        )

    def test_form_invalid_renewal_date_future(self):
        login = self.client.login(username='testuser2', password='12345')
        invalid_date_in_future = datetime.date.today() + datetime.timedelta(weeks=5)
        url = reverse(
            'renew-book-librarian',
            kwargs={'pk': self.bookinstance1.pk}
        )
        resp = self.client.post(url, {'renewal_date':invalid_date_in_future} )
        self.assertEqual(resp.status_code, 200)
        self.assertFormError(
            resp,
            'form',
            'renewal_date',
            'Invalid date - renewal more than 4 weeks ahead'
        )
    def test_form_renewal_date_initially_has_date_three_weeks_in_future(self):
        login = self.client.login(username='testuser2', password='12345')
        url = reverse(
            'renew-book-librarian',
            kwargs={'pk': self.bookinstance1.pk}
        )
        resp = self.client.get(url)
        date_3_weeks_in_future = datetime.date.today() + datetime.timedelta(weeks=3)
        self.assertEqual(
            resp.context['form'].initial['renewal_date'],
            date_3_weeks_in_future
        )