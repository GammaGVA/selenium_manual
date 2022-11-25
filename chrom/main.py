from selenium import webdriver
# from selenium.webdriver import Chrome
# from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys # Это не стал убирать
from time import sleep
import json

try:
    options = webdriver.ChromeOptions()
    options.add_argument(
        "user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36")
    # Говорим машине что мы такой user-agent

    options.add_argument("--disable-blink-features=AutomationControlled")
    # Отключаем видимость вебдрайвера.

    # options.headless = True - можно ещё вот так
    options.add_argument("--headless")
    # Работаем в фоновом режиме.

    service = webdriver.chrome.service.Service(r'/home/ivan/.ssh/selenium_manual/chrom/chromedriver')
    browser = webdriver.Chrome(service=service, options=options)
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
    # Скорее всего, сайт палит что я его парсю, надо попробовать через selenium кнопки искать. Так что код выше не подходит.
    # В первый раз это работало.

    sleep(2)
    number: int = int(browser.find_elements(by='class name', value='lnk-page')[-2].text)

    punkt = 1
    # Ввёл для отображения хода процесса, а то в фоновом не понятно что как идёт.

    for number_page in range(number):
        print(f'Делаем {punkt}/{number}')
        punkt += 1
        count = 0
        sleep(1)

        all_page = browser.find_elements(by='xpath', value='//div[@class="res-row"]')
        # Ушёл от супа, так стало попонятнее. Убрал мусорный элементы, дублировал инфу, теперь беру всё отсюда.

        for org in all_page:
            name_org = org.find_element(by='class name', value='op-excerpt').text.strip()
            info_org_list = org.find_element(by='class name', value="res-text").text.split(',')
            # Слеши "\" не реплесются в название, пробовал по всякому не получается.
            adress = []
            Dct = {name_org: {}}
            count += 1
            for i in info_org_list:
                if ':' in i:
                    point = i.split(':')[0].strip()
                    vale = i.split(':')[1].strip()
                    Dct[name_org].setdefault(point, vale)
                else:
                    adress += [i]
            if adress:
                Dct[name_org]['Адрес'] = ' '.join(adress).replace('  ', ' ').strip()
                # Сделал для ИП, от них адрес не тянется.

            # Столько провозился и не понимал, почему не всё пишется и много не полных словарей.
            # Я запись под for запихнул.
            if 'Дата прекращения деятельности' not in Dct[name_org]:
                with open(f'{name_orgs}.json', 'a', encoding='utf-8') as file:
                    json.dump(Dct, file, indent=4, ensure_ascii=False)
            else:
                with open(f'{name_orgs}_ликвидированные.json', 'a', encoding='utf-8') as file:
                    json.dump(Dct, file, indent=4, ensure_ascii=False)
            # Запись идёт криво, видимо json расчитан под запись одного словоря(скобки там в притирку получаются "конец пред словоря" - }{ - "начало след").
        browser.find_element(by='class name', value='lnk-page-next').click()
        # Тут раньше был косяк, искал по пути, и при новых значения name по страницам не переходило.
        sleep(2)
    print('Готово!')
except Exception as EX:
    print(EX)
finally:
    browser.close()
    browser.quit()

'''
В общих чертах гораздо удобнее чем request. На мой взгляд.
В теории не вижу даже суп использовать.

by="class name" у меня нигде не сработал, так что скорее всего буду использовать "xpath".
Всё заработало, руки выпримялись. Наш

Муторно что send_keys нельзя к одной переменной использовать дважды, но это просто увеличивает количество строк.

Не захотел дрочиться с текстом, вначале думал сделать json но у всех адрес разбит по разному.
Сделал json. Дальше попробовать в БД записать.

У кого-то нет запятых в адресе у кого-то есть, решил просто азы пока узнать и не ломать голову с группировкой данных.

Как же задолбала подмена данных на None. Всё же selenium не панацея, но я и сам виноват. Долблю по 100500 раз сервер.
А нет с подменой разобрался, всё таки панацея.
'''
