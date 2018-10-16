""" Test task № 1
    Simple tests for api
"""
# pylint:disable=redefined-outer-name


import pytest
import requests
from requests.auth import HTTPBasicAuth


USER = 'test_user'
PASSWORD = 'test_password'
HOST = 'http://localhost:7000'


@pytest.fixture(scope='function')
def auth_cookie():
    """ This fixture allows to get auth cookie. """

    url = '{0}/login'.format(HOST)
    auth = HTTPBasicAuth(USER, PASSWORD)
    result = requests.get(url, auth=auth)

    data = result.json()

    # Return auth_cookie to test:
    yield data['auth_cookie']


def test_check_login():
    """ This test checks that login REST API works fine. """

    url = '{0}/login'.format(HOST)

    # Send GET REST API request with basic auth:
    result = requests.get(url,
                          auth=HTTPBasicAuth(USER, PASSWORD))
    data = result.json()

    # Verify that server returns some auth cookie:
    assert result.status_code == 200
    assert data['auth_cookie'] > ''

def test_check_wrong_login():
    """ This test checks that fake login does not works fine. """

    user_fake = 'Evlampiy_1977'
    url = '{0}/login'.format(HOST)

    # Send GET REST API request with basic auth:
    result = requests.get(url,
                          auth=HTTPBasicAuth(user_fake, PASSWORD))


    # Verify that server returns 401:
    assert result.status_code == 401
    assert result.reason == 'UNAUTHORIZED'


def test_check_list_of_books_fake_cookie(auth_cookie):
    """ This test checks /books REST API function with fake cookie """

    url = '{0}/books'.format(HOST)
    fake_cookie = '485039457843563486uuuu5209456345764375634994587485785'
    result = requests.get(url, cookies={'my_cookie': fake_cookie})

    'INTERNAL SERVER ERROR'

    assert result.status_code == 500
    assert result.reason == 'INTERNAL SERVER ERROR'


def test_check_list_of_books(auth_cookie):
    """ This test checks /books REST API function.  """

    url = '{0}/books'.format(HOST)
    result = requests.get(url, cookies={'my_cookie': auth_cookie})
    data = result.json()

    assert result.status_code == 200
    assert isinstance(data, list)


def test_add_book(auth_cookie):
    """ Create new book and check that book was successfully created.

        Steps:
        1) Add new book
        2) Get list of all books
        3) Check that new book is presented in the list of all books

    """

    url = '{0}/add_book'.format(HOST)
    new_book = {'title': 'Book about QA', 'author': 'Me :)'}

    # Create new book:
    # Note: here we sending POST request with cookie and body!
    result = requests.post(url, data=new_book,
                           cookies={'my_cookie': auth_cookie})
    data = result.json()
    # Get id of created book:
    new_book['id'] = data['id']

    # Get list of books (GET request with cookie!):
    # host = 'http://localhost:7000'

    result2 = requests.get(HOST + '/books',
                           cookies={'my_cookie': auth_cookie})
    all_books = result2.json()

    # Verify that new book is presented in the list of books:
    assert new_book in all_books


def test_get_book(auth_cookie):
    """ Create new book,  and check that book was added.

        Steps:
        1) Create new book
        2) Get list of all books and verify that this book is presented
           in the list

    """

    url = '{0}/add_book'.format(HOST)
    new_book = {'title': 'Book about QA', 'author': 'Me :)'}

    # Create new book:
    result = requests.post(url, data=new_book,
                           cookies={'my_cookie': auth_cookie})
    data = result.json()
    # Get id of created book:
    new_book['id'] = data['id']


    # Get list of books:
    result = requests.get('{0}/books'.format(HOST),
                          cookies={'my_cookie': auth_cookie})
    list_of_all_books = result.json()

    # Verify that book is  presented in the list:
    assert new_book in list_of_all_books


def test_delete_book_does_not_exist(auth_cookie):
    """ Create new book, delete it and check that book was successfully deleted.

        Steps:
        1) Try to delete book with fake id
        3) Get list of all books and verify that the list is the same

    """

    fake_id = '123moskwa96877new'

    # Get list of books:
    result = requests.get('{0}/books'.format(HOST),
                          cookies={'my_cookie': auth_cookie})
    list_of_all_books_before = result.json()

    # Delete book (Note: DELETE REST API request with cookie!):
    url = '{0}/books/{1}'.format(HOST, fake_id)
    result = requests.delete(url,
                             cookies={'my_cookie': auth_cookie})

    # Get list of books:
    result = requests.get('{0}/books'.format(HOST),
                          cookies={'my_cookie': auth_cookie})
    list_of_all_books_after = result.json()

    # Verify that book is not presented in the list:
    assert (list_of_all_books_before) == (list_of_all_books_after)


def test_update_book(auth_cookie):
    """ Create new book, change title  and check that title of book was successfully changed.

        Steps:
        1) Create new book
        2) Change title of this book
        3) Get this book and verify that it has new name

    """

    url = '{0}/add_book'.format(HOST)
    old_title = 'Book for manager'
    new_book = {'title': old_title, 'author': 'Decker'}

    # Create new book:
    result = requests.post(url, data=new_book,
                           cookies={'my_cookie': auth_cookie})
    data = result.json()

    # Get id of created book:
    new_book['id'] = data['id']

  # Change name of book (Note: DELETE REST API request with cookie!):
    new_title = 'Book for QA'
    new_book_info = {'title': new_title, 'author': 'Decker'}
    url = '{0}/books/{1}'.format(HOST, new_book['id'])
    result = requests.put(url,data=new_book_info,
                             cookies={'my_cookie': auth_cookie})
    data_new = result.json()
    new_book_title= data_new['title']

    assert new_title == new_book_title


def test_delete_book(auth_cookie):
    """ Create new book, delete it and check that book was successfully deleted.

        Steps:
        1) Create new book
        2) Delete this book
        3) Get list of all books and verify that this book is not presented
           in the list

    """

    url = '{0}/add_book'.format(HOST)
    new_book = {'title': 'Book about QA', 'author': 'Me :)'}

    # Create new book:
    result = requests.post(url, data=new_book,
                           cookies={'my_cookie': auth_cookie})
    data = result.json()
    # Get id of created book:
    new_book['id'] = data['id']

    # Delete book (Note: DELETE REST API request with cookie!):
    url = '{0}/books/{1}'.format(HOST, new_book['id'])
    result = requests.delete(url,
                             cookies={'my_cookie': auth_cookie})

    # Get list of books:
    result = requests.get('{0}/books'.format(HOST),
                          cookies={'my_cookie': auth_cookie})
    list_of_all_books = result.json()

    # Verify that book is not presented in the list:
    assert new_book not in list_of_all_books


if __name__ == "__main__":
    # в PyCharm удобно запускать как обычный скрипт. Без командной строки
    pytest.main()
