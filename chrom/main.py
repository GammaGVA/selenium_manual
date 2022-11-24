from selenium import webdriver  # Потребовалось для options
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as BS
from time import sleep
import json

try:
    options = webdriver.ChromeOptions()
    options.add_argument(
        "user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36")
    options.add_argument("--disable-blink-features=AutomationControlled")
    browser = Chrome(service=Service(r'/home/ivan/.ssh/selenium_manual/chrom/chromedriver'), options=options)
    # Забыл про options, теперь доставил. Т.к. скрыл работу webdriver-а, вчера некоторые данные не получалось в супе получить, сегодня должно получиться.
    # Service тут используется т.к. selenium обновился и теперь так вот
    # В chrom два драйвера, т.к. чередую винду и линукс

    url = r'https://egrul.nalog.ru/index.html'
    browser.get(url=url)
    find_region = browser.find_element(by='name', value='query')

    sleep(2)

    name_orgs: str = input('Введите запрос на организации (например окология, хозяйство, буз): ')
    # name_orgs = 'ОТКРЫТОЕ АКЦИОНЕРНОЕ ОБЩЕСТВО ПО ПЕРЕРАБОТКЕ МОЛОКА "КУБАРУС-МОЛОКО"'

    find_inn = browser.find_element(by='xpath', value='//*[@id="query"]').send_keys(name_orgs)
    # Или могли имитировать ENTER find_inn.send_keys(Keys.ENTER), но два сенда нельзя на одну кнопку, или я не понял как
    browser.find_element(by='xpath', value='//*[@id="query"]').send_keys(Keys.ENTER)
    # sleep(1)
    # button = browser.find_element(by='xpath', value='//button[@type="submit"]')
    # button.click()

    # name_orgs = name_orgs.replace(' ', '_').replace(',', '_').replace('.', '')
    # pagination = BS(browser.page_source, 'lxml').find_all('a', class_='lnk-page')
    # Скорее всего сайт палит что я его парсю, надо попробовать через selenium кнопки искать. Так что код выше не подходит.

    sleep(2)
    number: int = int(browser.find_elements(by='class name', value='lnk-page')[-2].text)

    for number_page in range(number):
        count = 0
        sleep(1)
        soup = BS(browser.page_source, 'lxml')
        # Слетела lxml долго не мог понять почему вчера работало, а сегодня нет (pip install lxml)
        orgs = soup.find_all('a', class_='op-excerpt')
        all_page = soup.find_all('div', class_='res-row')
        for org in all_page:
            info_org = org.find("div", class_="res-text").text
            info_org_lst = info_org.split(',')
            nme_org = orgs[count].text.strip()
            # Слеши "\" не реплесются в название, пробовал по всякому не получается.
            adress = []
            Dct = {nme_org: {}}
            count += 1
            for i in info_org_lst:
                if ':' in i:
                    point = i.split(':')[0].strip()
                    vale = i.split(':')[1].strip()
                    Dct[nme_org].setdefault(point, vale)
                else:
                    adress += [i]
            Dct[nme_org]['Адрес'] = ' '.join(adress).replace('  ', ' ').strip()
            # Столько провозился и не понимал почему не всё пишется и много не полных словарей.
            # Я запись под for запихнул.
            if 'Дата прекращения деятельности' not in info_org:
                with open(f'{name_orgs}.json', 'a', encoding='utf-8') as file:
                    json.dump(Dct, file, indent=4, ensure_ascii=False)
            else:
                with open(f'{name_orgs}_ликвидированные.json', 'a', encoding='utf-8') as file:
                    json.dump((Dct, '\n'), file, indent=4, ensure_ascii=False)
            # Запись идёт криво, видимо json расчитан под запись одного словоря(скобки там в притирку получаются "конец пред словоря" - }{ - "начало след").
        browser.find_element(by='class name', value='lnk-page-next').click()
        # Тут раньше был косяк, искал по пути, и при новых значения name по страницам не переходило.
        sleep(2)
except Exception as EX:
    print(EX)
finally:
    browser.close()
    browser.quit()

'''
В общих чертах гораздо удобнее чем request. На мой взгляд.

by="class name" у меня нигде не сработал, так что скорее всего буду использовать "xpath".
Всё заработало, руки выпримялись.

Муторно что send_keys нельзя к одной переменной использовать дважды, но это просто увеличивает количество строк.

Не захотел дрочиться с текстом, вначале думал сделать json но у всех адрес разбит по разному.
Сделал json. Дальше попробовать в БД записать.

У кого-то нет запятых в адресе у кого-то есть, решил просто азы пока узнать и не ломать голову с группировкой данных.

Как же задолбала подмена данных на None. Всё же selenium не панацея, но я и сам виноват. Долблю по 100500 раз сервер.
А нет с подменой разобрался, всё таки панацея.
'''
