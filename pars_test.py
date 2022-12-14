from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from time import sleep


def mask():
    try:
        options = webdriver.ChromeOptions()
        options.add_argument(
            "user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36")
        # Говорим машине что мы такой user-agent

        options.add_argument("--disable-blink-features=AutomationControlled")
        # Отключаем видимость вебдрайвера.

        options.add_argument("--headless")
        # Работаем в фоновом режиме.

        browser = Chrome(service=Service(r'/home/ivan/.ssh/selenium_manual/chrom/chromedriver'), options=options)
        url = 'https://intoli.com/blog/not-possible-to-block-chrome-headless/chrome-headless-test.html'
        browser.get(url=url)
        sleep(10)
    except Exception:
        print(Exception)
    finally:
        browser.close()
        browser.quit()
