import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC


def do_job():

    chrome_options = Options()
    chrome_options.add_argument("--window-size=1400,900")
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--log-level=DEBUG')
    executable_path='C:\\PF\\selen_chrome\\chromedriver.exe'
    browser = webdriver.Chrome(executable_path=executable_path,
                               chrome_options=chrome_options)

 
    browser.get("http://www.ya.ru")
    assert "Яндекс" in browser.title

 
    elem = WebDriverWait(browser, 10).until(lambda driver: driver.find_element_by_id("text"))

    elem.send_keys("testing")
    elem.send_keys(Keys.RETURN)
    
	page_loaded = False
    while not page_loaded:
        page_loaded = browser.execute_script("return document.readyState == 'complete';")
        time.sleep(0.3)
    
    filename="file.png"
    browser.save_screenshot(filename)

    browser.quit()

if __name__ == '__main__':
    do_job()