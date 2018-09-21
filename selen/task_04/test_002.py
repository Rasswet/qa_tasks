import pytest
import time
# import win_unicode_console
# win_unicode_console.enable()

# This is a simple example of PyTest test case with Selenium
# should install pytest-selenium
#
# To run test cases, execute the following commands:

# cd qa_python перейти в папку где лежит этот файл.
# командная строка для Linux
# pytest -v --driver Chrome --driver-path /usr/bin/chromedriver test_pytest_002.py
# командная строка для Windows
# pytest -v --driver Chrome --driver-path 'C:\\PF\\selen_chrome\\chromedriver.exe' test_pytest_002.py

@pytest.fixture
def selenium(selenium):
    selenium.implicitly_wait(20)
    # selenium.maximize_window()
    return selenium


@pytest.fixture
def chrome_options(chrome_options):
    # chrome_options.binary_location = '/usr/bin/google-chrome-stable'
    # chrome_options.add_argument('--headless')
    # chrome_options.add_argument('--no-sandbox') # перестает висеть в фоне после закрытия
    chrome_options.add_argument('--log-level=DEBUG')

    return chrome_options


@pytest.fixture(scope="function")
def web_browser(request, selenium):
    browser = selenium
    # browser.set_window_size(1400, 1000)

    # Return browser instance to test case:
    yield browser
    
    try:
        # Close browser window:
        browser.quit()
    except:
        print("I can't close your browser")
        # pass  # just ignore any errors if we can't close the browser.


@pytest.mark.parametrize('str_check', [u'Гугл', u"Яндекс"])
def test_with_some_parameters(str_check, web_browser):
    """ This is very simple example of test with parameters.
        Note: parameter 'web_browser' - is the fixture of PyTest,
              which will automaticall start browser and return
              WebDriver element to the test case.

        It will be executed 2 times with the following parameters:
         1) a = 'Гугл'
         2) a = 'Яндекс'
        So, this test will fail only once :)
    """
    
    web_browser.get('https://ya.ru')

    assert str_check in web_browser.title


if __name__ == "__main__":
    # в PyCharm удобно запускать как обычный скрипт. Без командной строки
    pytest.main()
