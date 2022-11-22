from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as BS
from time import sleep

try:
    browser = Chrome(service=Service(r'/home/ivan/.ssh/selenium_manual/chrom/chromedriver'))
    # Service тут используется т.к. selenium обновился и теперь так вот
    # В chrom два драйвера, т.к. чередую винду и линукс
    url = r'https://egrul.nalog.ru/index.html'
    browser.get(url=url)
    find_region = browser.find_element(by='name', value='query')
    sleep(1)
    name_orgs = 'молоко'
    find_inn = browser.find_element(by='xpath', value='//*[@id="query"]').send_keys(name_orgs)
    # Или могли имитировать ENTER find_inn.send_keys(Keys.ENTER), но два сенда нельзя на одну кнопку, или я не понял как
    browser.find_element(by='xpath', value='//*[@id="query"]').send_keys(Keys.ENTER)
    # sleep(1)
    # button = browser.find_element(by='xpath', value='//button[@type="submit"]')
    # button.click()
    name_orgs = name_orgs.replace(' ', '_').replace(',', '_').replace('.', '')

    for number_page in range(114):
        sleep(1)
        soup = BS(browser.page_source, 'lxml')
        all_page = soup.find_all('div', class_='res-row')
        with open(f'{name_orgs}.text', 'a', encoding='utf-8') as file:
            for org in all_page:
                if 'Дата прекращения деятельности' not in org.find("div", class_="res-text").text:
                    file.write(
                        f'{org.find("a", class_="op-excerpt").text}:{org.find("div", class_="res-text").text}\n{"_" * 100}\n')
                else:
                    with open(f"ликвид_{name_orgs}.text", "a", encoding="utf-8") as F:
                        F.write(
                            f'{org.find("a", class_="op-excerpt").text}:{org.find("div", class_="res-text").text}\n{"_" * 100}\n')
            file.write("!" * 50 + '\n')
        browser.find_element(by='xpath', value='/html/body/div[1]/div[3]/div/div[1]/div[5]/ul/li[13]/a').click()
        sleep(2)
except Exception as EX:
    print(EX)
finally:
    browser.close()
    browser.quit()

'''
В общих чертах даже удобнее чем request. На мой взгляд по крайней мере.
by="class name" у меня нигде не сработал, так что скорее всего буду использовать "xpath".
Муторно что send_keys нельзя к одной переменной использовать дважды, но это просто увеличивает количество строк.
Не захотел дрочиться с текстом, вначале думал сделать json но у всех адрес разбит по разному.
У когото нет запятых в адресе у кагото есть, рещил просто азы пока узнать и не ломать голову с группировкой данных.
'''
