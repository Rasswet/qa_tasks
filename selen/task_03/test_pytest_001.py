import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC


def get_browser():

    chrome_options = Options()
    chrome_options.add_argument("--window-size=1400,900")
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--log-level=DEBUG')
    executable_path='C:\\PF\\selen_chrome\\chromedriver.exe'
    browser = webdriver.Chrome(executable_path=executable_path,
                               options=chrome_options)

    return browser


def test_lesson_1():

    browser = get_browser()
    browser.get("http://www.ya.ru")
    assert "Яндекс" in browser.title
    browser.quit()

def test_which_should_always_fail():
    """
        This test will always fail, it is just an example :)
    """
    browser = get_browser()
    browser.get("http://www.google.ru")
    expected = True
    if "Яндекс" in browser.title:
        actual = True
    else:
        actual = False

    assert expected == actual, 'Expected not equal to Actual!'

    browser.quit()

if __name__ == "__main__":
    pytest.main()
