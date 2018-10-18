""" Test task
    Simple tests for api
"""
# pylint:disable=redefined-outer-name

import pytest

# from .utils import add_book
# from .utils import get_all_books
# from .utils import get_book
# from .utils import update_book
# from .utils import delete_book
# from .utils import validate_uuid4

from utils import add_book
from utils import get_all_books
from utils import get_book
from utils import update_book
from utils import delete_book
from utils import validate_uuid4
from utils import host
from utils import auth
from utils import put

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
@pytest.mark.parametrize('author', [ u'Пушкин'])
def test_delete_book(title, author):
    # Create new book:
    new_book = add_book({'title': '', 'author': ''})

    # book_id=u'УтроСтарыйХооббитВасилий'


    book_id = new_book['id']

    # Get list of all books:
    all_books_before = get_all_books()

    # Update book attributes:
    delete_book(book_id)

    all_books_after = get_all_books()

    # Get info about this book:
    book = get_book(book_id)

    assert len(book)==0
    assert len(all_books_before)-1 == len(all_books_after)

@pytest.mark.parametrize('book_id', [u'SomeRareBook'])
# @pytest.mark.parametrize('book_id', [u'УтроСтарыйХооббитВасилий'])
def test_delete_book_negative(book_id):
    # Get list of all books:
    all_books_before = get_all_books()

    # book_id = 'VasiliyOldHobbyt'
    # Update book attributes:
    delete_book(book_id)

    all_books_after = get_all_books()

    assert len(all_books_before) == len(all_books_after)


@pytest.mark.parametrize('title', ['"', 'test', u'тест'])
@pytest.mark.parametrize('author', ['', 'Teodor Drayzer', u'Пушкин'])
def test_update_book(title, author):
    # Create new book:
    new_book = add_book({'title': '', 'author': ''})
    book_id = new_book['id']

    # Update book attributes:
    update_book(book_id, {'title': title, 'author': author})

    # Get info about this book:
    book = get_book(book_id)

    # Verify that changes were applied correctly:
    assert book['title'] == title
    assert book['author'] == author


@pytest.mark.parametrize('book_id', [u'090909090999000999'])
@pytest.mark.parametrize('title', [ u'тест_нога'])
@pytest.mark.parametrize('author', [ u'тест__нога'])
def test_negative_update_book(book_id,title, author):

    # Try to update book attributes:

    url = '{0}/books/{1}'.format(host, book_id)
    body = {'title': title, 'author': author}
    response = put(url, cookies=auth(), body=body)

    # Verify that changed nothing:
    assert response.status_code== 404



if __name__ == "__main__":
    # useful for PyCharm
    pytest.main()
