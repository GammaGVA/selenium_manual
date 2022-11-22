from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys

from time import sleep

browser = Chrome(service=Service(r'E:\python\selenium_manual\chrom\chromedriver.exe'))
url = r'https://egrul.nalog.ru/index.html'
browser.get(url=url)
find_region = browser.find_element()
sleep(3)
find_inn = browser.find_element(by='xpath', value='//*[@id="query"]').send_keys('Молоко')
sleep(3)