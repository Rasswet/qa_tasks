'''
You can find simple example of the ussage Selenium with PyTest in this file.

# More info about pytest-selenium:
#    https://pytest-selenium.readthedocs.io/en/latest/user_guide.html
#
# How to run:
#  1) Download geko driver for Chrome here:
#     https://chromedriver.storage.googleapis.com/index.html?path=2.43/
#  2) Install all requirements:
#     pip install -r requirements.txt
#  3) Run tests:
#     python3 -m pytest -v --driver Chrome --driver-path /tests/chrome test_selenium_simple.py

'''

import time
import pytest

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys


@pytest.fixture
def selenium(selenium):
    'Selenium fixture'
    selenium.implicitly_wait(20)
    # selenium.maximize_window()
    return selenium


@pytest.fixture
def chrome_options(chrome_options):
    'Create chrome option'
    # chrome_options.binary_location = '/usr/bin/google-chrome-stable'
    # chrome_options.add_argument('--headless')
    # chrome_options.add_argument('--no-sandbox') # stop working in background
    chrome_options.add_argument('--log-level=DEBUG')

    return chrome_options


@pytest.fixture(scope="function")
def web_browser(request, selenium):
    ' Create web-browser'
    browser = selenium
    browser.set_window_size(1400, 1000)

    # Return browser instance to test case:
    yield browser

    try:
        # Close browser window:
        browser.quit()
    except Exception as err:
        print("I can't close your browser")
        # pass  # just ignore any errors if we can't close the browser.


@pytest.mark.parametrize('url_check', [u'https://www.mvideo.ru/'])
@pytest.mark.parametrize('title', [u'М.Видео'])
def test_with_some_parameters(url_check, title, web_browser):
    """ Search some phrase in google and make a screenshot of the page. """

    web_browser.get(url_check)

    assert title in web_browser.title

    elem = WebDriverWait(web_browser, 10).until(lambda driver: driver.find_element_by_name("Ntt"))
    # elem.clear()
    item_for_search = "De Longhi ECAM 22.360"
    elem.send_keys(item_for_search)
    elem.send_keys(Keys.RETURN)
    time.sleep(2)

    xpath_for_first = r"(//*[contains(@class,'product-tile-title-link sel-product-tile-title')])[1]"
    elem = WebDriverWait(web_browser, 10).until(lambda driver: driver.find_element_by_xpath(xpath_for_first))
    assert item_for_search in elem.text

    elem.send_keys(Keys.RETURN)
    # time.sleep(2)

    assert item_for_search in web_browser.title


if __name__ == "__main__":
    # easy in PyCharm
    pytest.main()
