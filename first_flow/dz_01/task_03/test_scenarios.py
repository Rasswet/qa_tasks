""" Test task
    Simple tests for api

    How to run 1 test?
    Example (from test dir): python -m pytest test_scenarios.py -k test_negative_update_book

"""
# pylint:disable=redefined-outer-name

import pytest


from .utils import add_book
from .utils import get_all_books
from .utils import get_book
from .utils import update_book
from .utils import delete_book
from .utils import validate_uuid4
from .utils import host
from .utils import auth
from .utils import put


@pytest.mark.parametrize('title', ['', 'test', u'тест'])
@pytest.mark.parametrize('author', ['', 'Teodor Drayzer', u'Пушкин'])
def test_create_new_book(title, author):
    """ Check 'create book' method with different values of
        Title and Author.
    """

    book = {'title': title, 'author': author}
    new_book = add_book(book)

    all_books = get_all_books()

    assert new_book in all_books


def test_get_list_of_books():
    """ Check that 'get books' method returns correct list of books. """

    # Create two books, just to make sure books will be correctly
    # added to the list:
    add_book({'title': '', 'author': ''})
    add_book({'title': '1', 'author': '2'})

    # Get list of all books:
    all_books = get_all_books()

    # Check that every book in the list has all required attributes:
    for book in all_books:
        assert 'title' in book
        assert 'author' in book
        assert validate_uuid4(book['id'])

    print(all_books)
    # Make sure that the list has at least 2 books:
    assert len(all_books) >= 2


@pytest.mark.parametrize('title', [u'тест'])
@pytest.mark.parametrize('author', [u'Пушкин', 'Chase'])
def test_delete_book(title, author):
    """ Check that 'get books' method returns correct list of books. """

    new_book = add_book({'title': title, 'author': author})
    book_id = new_book['id']

    all_books_before = get_all_books()

    delete_book(book_id)

    all_books_after = get_all_books()

    book = get_book(book_id)

    assert book == dict()
    assert len(all_books_before)-1 == len(all_books_after)


@pytest.mark.parametrize('book_id', [u'SomeRareBook_id_'])
def test_delete_book_negative(book_id):
    """ Check that we can not delete book in negative case. """

    # Get list of all books:
    all_books_before = get_all_books()

    delete_book(book_id)

    all_books_after = get_all_books()

    assert len(all_books_before) == len(all_books_after)


@pytest.mark.parametrize('title', ['"', 'test', u'тест'])
@pytest.mark.parametrize('author', ['', 'Teodor Drayzer', u'Блок'])
def test_update_book(title, author):
    """ Check that we can update book info. """

    new_book = add_book({'title': '', 'author': ''})
    book_id = new_book['id']

    update_book(book_id, {'title': title, 'author': author})

    book = get_book(book_id)

    # Verify that changes were applied correctly:
    assert book['title'] == title
    assert book['author'] == author


@pytest.mark.parametrize('book_id', [u'0909090909990009997'*50])
@pytest.mark.parametrize('title', [u'тест_негатив_заголовок_'])
@pytest.mark.parametrize('author', [u'тест__негатив author_'])
def test_negative_update_book(book_id, title, author):
    """ Check that we can not update book info. """

    # Try to update book attributes. Negative case:
    url = '{0}/books/{1}'.format(host, book_id)
    body = {'title': title, 'author': author}
    response = put(url, cookies=auth(), body=body)

    # Verify that changed nothing:
    assert response.status_code == 404

if __name__ == "__main__":
    # в PyCharm удобно запускать как обычный скрипт. Без командной строки
    pytest.main()
