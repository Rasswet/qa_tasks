import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def do_job():

    chrome_options = Options()
    chrome_options.add_argument("--window-size=1400,900")
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--log-level=DEBUG')
    executable_path='C:\\PF\\selen_chrome\\chromedriver.exe'
    browser = webdriver.Chrome(executable_path=executable_path,
                               chrome_options=chrome_options)

    time.sleep(2)
    browser.quit()

if __name__ == '__main__':
    do_job()